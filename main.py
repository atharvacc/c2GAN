import tensorflow as tf


from datetime import datetime
import os
import logging
from scipy import misc
import numpy as np

from cycleGAN_utils.model import CycleGAN
from cycleGAN_utils.reader import Reader
from cycleGAN_utils.utils import ImagePool

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string('type', 'train', 'the type of code, default: train')
tf.flags.DEFINE_string('project', 'apple2orange',
                       'project name , default: apple2orange') 
tf.flags.DEFINE_string('loss_type', 'black2black', 'the type of code, default: black2black || black2white || white2white')

tf.flags.DEFINE_integer('batch_size', 1, 'batch size, default: 1')
tf.flags.DEFINE_integer('image_size', 256, 'image size, default: 128')
tf.flags.DEFINE_bool('use_lsgan', True,
                     'use lsgan (mean squared error) or cross entropy loss, default: True')
tf.flags.DEFINE_string('norm', 'instance',
                       '[instance, batch] use instance norm or batch norm, default: instance')
tf.flags.DEFINE_integer('lambda1', 10,
                        'weight for forward cycle loss (X->Y->X), default: 10')
tf.flags.DEFINE_integer('lambda2', 10,
                        'weight for backward cycle loss (Y->X->Y), default: 10')
tf.flags.DEFINE_float('learning_rate', 2e-4,
                      'initial learning rate for Adam, default: 0.0002')
tf.flags.DEFINE_float('beta1', 0.5,
                      'momentum term of Adam, default: 0.5')
tf.flags.DEFINE_float('pool_size', 50,
                      'size of image buffer that stores previously generated images, default: 50')
tf.flags.DEFINE_integer('ngf', 64,
                        'number of gen filters in first conv layer, default: 64')

tf.flags.DEFINE_string('X', 'data/training_images/tfrecords/apple.tfrecords',
                       'X tfrecords file for training, default: data/tfrecords/apple.tfrecords')
tf.flags.DEFINE_string('Y', 'data/training_images/tfrecords/orange.tfrecords',
                       'Y tfrecords file for training, default: data/tfrecords/orange.tfrecords')
tf.flags.DEFINE_string('load_model', None,
                        'folder of saved model that you wish to continue training (e.g. 20170602-1936), default: None')

tf.flags.DEFINE_string('GPU', '1',
                        'folder of saved model that you wish to continue training (e.g. 20170602-1936), default: None')

tf.flags.DEFINE_integer("channels", 3, "the channels of input image, default: 3")
tf.flags.DEFINE_integer("epoch", 5, "Number of epoch for training, default: 5e4")

tf.flags.DEFINE_integer("unet_conv_size", 3, "Convolution kernel size in encoding and decoding paths, default: 3")
tf.flags.DEFINE_float("unet_dropout_ratio", 0.5, "Drop out ratio, default: 0.5")


def train():
  # whether you load parameters
  if FLAGS.load_model is not None:
    checkpoints_dir = "checkpoints/" + FLAGS.load_model.lstrip("checkpoints/")
  else:
    current_time = datetime.now().strftime("%Y%m%d-%H%M")
    checkpoints_dir = "checkpoints/{}".format(current_time)
    try:
      os.makedirs(checkpoints_dir)
    except os.error:
      pass

  # make dir to save the images generated by model
  # if you train the model, the images generated by model will be save in 'fake' folder
  # if you test your model you have trained, the images will be save in 'result' folder
  if FLAGS.type == 'train':
    fake_folder = FLAGS.project+'_fake'+datetime.now().strftime("%Y%m%d-%H%M")
    fake_x_folder = 'data/fake_images/'+fake_folder+'/'+FLAGS.project+'_fake_x'
    fake_y_folder = 'data/fake_images/'+fake_folder+'/'+FLAGS.project+'_fake_y'
    if os.path.exists('data/fake_images') is False:
      os.makedirs('data/fake_images')
    if os.path.exists(fake_x_folder) is False:
      os.makedirs(fake_x_folder)
    if os.path.exists(fake_y_folder) is False:
      os.makedirs(fake_y_folder)
  
  if FLAGS.type == 'test':
    fake_folder=FLAGS.project+'_result'+datetime.now().strftime("%Y%m%d-%H%M")
    fake_x_folder = 'data/inferred_images/'+fake_folder+'/'+FLAGS.project+'_inferred_x'
    fake_y_folder = 'data/inferred_images/'+fake_folder+'/'+FLAGS.project+'_inferred_y'
    if os.path.exists('data/inferred_images') is False:
      os.makedirs('data/inferred_images')
    if os.path.exists(fake_x_folder) is False:
      os.makedirs(fake_x_folder)
    if os.path.exists(fake_y_folder) is False:
      os.makedirs(fake_y_folder)

  graph = tf.Graph()
  with graph.as_default():
    cycle_gan = CycleGAN(
        X_train_file=FLAGS.X,
        Y_train_file=FLAGS.Y,
        batch_size=FLAGS.batch_size,
        image_size=FLAGS.image_size,
        use_lsgan=FLAGS.use_lsgan,
        norm=FLAGS.norm,
        lambda1=FLAGS.lambda1,
        lambda2=FLAGS.lambda2,
        learning_rate=FLAGS.learning_rate,
        beta1=FLAGS.beta1,
        ngf=FLAGS.ngf,
        loss_type=FLAGS.loss_type,
        for_type=FLAGS.type,
        total_epoch=FLAGS.epoch,
        channels=FLAGS.channels
    )
    G_loss, D_Y_loss, F_loss, D_X_loss, fake_y, fake_x, fake_y_name, fake_x_name,x,y,test_loss,saliency_rate = cycle_gan.model()
    optimizers = cycle_gan.optimize(G_loss, D_Y_loss, F_loss, D_X_loss)

    summary_op = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter(checkpoints_dir, graph)
    saver = tf.train.Saver()

  with tf.Session(graph=graph) as sess:
    if FLAGS.load_model is not None:
      checkpoint = tf.train.get_checkpoint_state(checkpoints_dir)
      meta_graph_path = checkpoint.model_checkpoint_path + ".meta"
      restore = tf.train.import_meta_graph(meta_graph_path)
      restore.restore(sess, tf.train.latest_checkpoint(checkpoints_dir))
      step = int(meta_graph_path.split("-")[2].split(".")[0])
    else:
      sess.run(tf.global_variables_initializer())
      step = 0

    init=step
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

    try:
      fake_Y_pool = ImagePool(FLAGS.pool_size)
      fake_X_pool = ImagePool(FLAGS.pool_size)

      while not coord.should_stop():
        fake_y_val, fake_x_val, fake_y_name_val, fake_x_name_val= sess.run([fake_y, fake_x, fake_y_name, fake_x_name])
        if FLAGS.type == 'train':
          if step % 100 == 0:
            fake_y_img=np.squeeze(fake_y_val)
            fake_y_path=fake_y_folder + '/' + str(step)+str(fake_y_name_val)+'.png'
            misc.imsave(fake_y_path,fake_y_img)
            fake_x_img=np.squeeze(fake_x_val)
            fake_x_path =fake_x_folder + '/' + str(step)+str(fake_y_name_val)+'.png'
            misc.imsave(fake_x_path,fake_x_img)

        if FLAGS.type == 'test':
          if step % 1 == 0:
            fake_y_img=np.squeeze(fake_y_val)
            fake_y_path = fake_y_folder + '/' + str(fake_y_name_val)+'+'+str(step)+'.png'
            misc.imsave(fake_y_path,fake_y_img)
            fake_x_img = np.squeeze(fake_x_val)
            fake_x_path = fake_x_folder + '/' + str(fake_x_name_val)+'+'+str(step)+'.png'
            misc.imsave(fake_x_path,fake_x_img)
          
        # train
        if FLAGS.type == 'train':
          _, G_loss_val, D_Y_loss_val, F_loss_val, D_X_loss_val, test_loss_val,saliency_rate_val, summary = (
              sess.run(
                  [optimizers, G_loss, D_Y_loss, F_loss, D_X_loss,test_loss,saliency_rate, summary_op],
                  feed_dict={cycle_gan.fake_y: fake_Y_pool.query(fake_y_val),
                             cycle_gan.fake_x: fake_X_pool.query(fake_x_val),
                             cycle_gan.epoch_num: step}
              )
          )

          train_writer.add_summary(summary, step)
          train_writer.flush()

        if FLAGS.type == 'train':
          if step % 100 == 0:
            logging.info('-----------Step %d:-------------' % step)
            logging.info('  G_loss   : {}'.format(G_loss_val))
            logging.info('  D_Y_loss : {}'.format(D_Y_loss_val))
            logging.info('  F_loss   : {}'.format(F_loss_val))
            logging.info('  D_X_loss : {}'.format(D_X_loss_val))
            logging.info('  test_loss : {}'.format(test_loss_val))
            logging.info('  saliency_rate : {}'.format(saliency_rate_val))
        
        if FLAGS.type == 'test':
          if step % 100 == 0:
            logging.info('-----------Step %d:-------------' % step)

        if FLAGS.type == 'train':
          if step % 10000 == 0:
            save_path = saver.save(sess, checkpoints_dir + "/model.ckpt", global_step=step)
            logging.info("Model saved in file: %s" % save_path)

        step += 1

        if step>=FLAGS.epoch+init:
          break
    except KeyboardInterrupt:
      logging.info('Interrupted')
      coord.request_stop()
    except Exception as e:
      coord.request_stop(e)
    finally:
      if FLAGS.type == 'train':
        save_path = saver.save(sess, checkpoints_dir + "/model.ckpt", global_step=step)
      logging.info("Model saved in file: %s" % save_path)
      # When done, ask the threads to stop.
      coord.request_stop()
      coord.join(threads)

def main(unused_argv):
  train()

if __name__ == '__main__':
  os.environ["CUDA_VISIBLE_DEVICES"] = FLAGS.GPU
  logging.basicConfig(level=logging.INFO)
  tf.app.run()
