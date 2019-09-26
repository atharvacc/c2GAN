import tensorflow as tf
import random
import os
import numpy as np 
import skimage as ski 
from PIL import Image

try:
  from os import scandir
except ImportError:
  from scandir import scandir
    

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string('project', 'apple2orange',
                       'project name , default: apple2orange') 
tf.flags.DEFINE_string('type', 'train',
                       'data for what , default: train') 
tf.flags.DEFINE_string('X', 'apple',
                       'X object name, default: apple')
tf.flags.DEFINE_string('Y', 'orange',
                       'Y object name, default: orange')

tf.flags.DEFINE_string('X_input_dir', 'data/'+FLAGS.project+'/'+FLAGS.type+'A',
                       'X input directory, default: data/apple2orange/trainA')
tf.flags.DEFINE_string('Y_input_dir', 'data/'+FLAGS.project+'/'+FLAGS.type+'B',
                       'Y input directory, default: data/apple2orange/trainB')
                       
tf.flags.DEFINE_string('X_output_file', 'data/tfrecords/'+FLAGS.X+'.tfrecords',
                       'X output tfrecords file, default: data/tfrecords/apple.tfrecords')
tf.flags.DEFINE_string('Y_output_file', 'data/tfrecords/'+FLAGS.Y+'.tfrecords',
                       'Y output tfrecords file, default: data/tfrecords/orange.tfrecords')
                       
tf.flags.DEFINE_string('image_format', '.png',
                       'Y output tfrecords file, default: data/tfrecords/orange.tfrecords')


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def _bytes_feature(value):
  """Wrapper for inserting bytes features into Example proto."""
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _float_feature(value):
  """Wrapper for inserting bytes features into Example proto."""
  return tf.train.Feature(bytes_list=tf.train.FloatsList(value=[value]))

def _convert_to_example(file_path, image_buffer):
  """Build an Example proto for an example.
  Args:
    file_path: string, path to an image file, e.g., '/path/to/example.JPG'
    image_buffer: string, JPEG encoding of RGB image
  Returns:
    Example proto
  """
  file_name = file_path.split('/')[-1]

  example = tf.train.Example(features=tf.train.Features(feature={
      'image/file_name': _bytes_feature(tf.compat.as_bytes(os.path.basename(file_name))),
      'image/encoded_image': _bytes_feature((image_buffer))
    }))
  return example

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def data_reader(input_dir,shuffle=True):
  """Read images from input_dir then shuffle them
  Args:
    input_dir: string, path of input dir, e.g., /path/to/dir
  Returns:
    file_paths: list of strings
  """

  file_paths = []
  if FLAGS.type+'A' in input_dir:
    for img_file in scandir(FLAGS.X_input_dir):
      if img_file.name.endswith('png') and img_file.is_file():
        file_paths.append(img_file.path)
  if FLAGS.type+'B' in input_dir:
    for img_file in scandir(FLAGS.Y_input_dir):
      if img_file.name.endswith('png') and img_file.is_file():
        file_paths.append(img_file.path)

  if shuffle:
    # Shuffle the ordering of all image files in order to guarantee
    # random ordering of the images with respect to label in the
    # saved TFRecord files. Make the randomization repeatable.
    shuffled_index = list(range(len(file_paths)))
    random.seed(12345)
    random.shuffle(shuffled_index)

    file_paths = [file_paths[i] for i in shuffled_index]

  return file_paths

def data_writer(input_dir, output_file):
  """Write data to tfrecords
  """
  if FLAGS.type+'A' in input_dir:
    file_paths = data_reader(FLAGS.X_input_dir)
  if FLAGS.type+'B' in input_dir:
    file_paths = data_reader(FLAGS.Y_input_dir)
  # create tfrecords dir if not exists
  output_dir = os.path.dirname(output_file)
  try:
    os.makedirs(output_dir)
  except os.error as e:
    pass
  images_num = len(file_paths)
  # dump to tfrecords file
  writer = tf.python_io.TFRecordWriter(output_file)

  for i in range(len(file_paths)):
    file_path = file_paths[i]

    with tf.gfile.FastGFile(file_path, 'rb') as f:
      image_data = f.read()

    example = _convert_to_example(file_path, image_data)
    writer.write(example.SerializeToString())

    if i % 100 == 0:
      print("Processed {}/{}.".format(i, images_num))
  print("Done.")
  writer.close()

def main(unused_argv):
  print("Convert A data to tfrecords...")
  data_writer(FLAGS.X_input_dir, FLAGS.X_output_file)
  print("Convert B data to tfrecords...")
  data_writer(FLAGS.Y_input_dir, FLAGS.Y_output_file)

if __name__ == '__main__':
  tf.app.run()
