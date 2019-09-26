## Position available

CycleGAN, as one of the most enlightening and startling strategy for neural network training, promises to perform a significant function in data-driven computational microscopy, including virtual staining etc. We hope that this method will offer potential for enlightening the utilizer of microscope. For more information please follow **this link**.

## CycleGAN model

A python code for constraint cycleGAN aims at addressing problems during the imaging
procedure of microscopy.

You can find the cycleGAN paper **here**.  Next we will mentor you step by step how to implement our computational model.

## Directory structure

The file structure is shown below:

```
cycleGAN
|---checkpoints
|	|---project_name+time  #creat by code#
|---|---|---meta
|---|---|---index
|---|---|---ckpt
|---data
|---|---isotrpic  #project_name#
|---|---|---trainA
|---|---|---trainB
|---|---|---testA
|---|---|---testB
|---fake
|---|---project_name+time
|---|---|---fake_x
|---|---|---fake_y
|---result
|---|---project_name+time
|---|---|---fake_x
|---|---|---fake_y
|---discriminator.py
|---export_graph.py
|---generator,py
|---inference.py
|---model.py
|---ops.py
|---preprocess.py
|---reader.py
|---main.py
```

## Environment

* ubuntu 16.0 + python 3.6.2 + Tensorflow 1.10.0 
* numpy 1.16.2 + scipy 0.18.1
* NVIDIA GPU + cuda

## Building environment

Open the terminal of ubuntu system.

* Install python 

```
$ apt-get install python 3.6
```

* Build anaconda environment

```
$ conda create -n tensorflow python=3.6
```

* Install tensorflow

```
$ source activate tensorflow
$ cd Download 
$ pip install --ignore-installed --upgrade tensorflow-1.3.0-py3-none-linux_x86_64.whl
```

* Test if the installation is successful

```
$ python
>>> import tensorflow as tf    
>>> hello = tf.constant("Hello World, TensorFlow!")
>>> sess = tf.Session()
>>> print(sess.run(hello))
```

* Install necessary packages

```
$ pip install scipy=0.18.1
$ pip install numpy=1.16.2
```

## Data processing

* You can download some data for demo code from **our web**. You can also download these raw data from **the table**.

| Project | Link |
| :-----: | :--: |
|         |      |
|         |      |
|         |      |

* Transform your pictures from '.tif' to '.png' and divide the dataset into training data and test data. Usually we use 65%~80% of the dataset as the training data and 20%~35% of the dataset as the testing data. The put training A dataset at the 'trainA' folder, training B dataset at the 'trainB' folder, testing A dataset at the 'testA' folder and testing B dataset at the 'testB' folder.

## For training

Write the training data into tfrecords

```
$ python preprocess.py --project 1_Isotropic_Liver --type train
```

or

```
$ python preprocess.py --project 1_Isotropic_Liver
```

Begin your train

```
$ python main.py
```

If you want to change the default parameter depend on yourself data , you can do this by the command line, for example:

```
$ python main.py  --project 1_Isotropic_Liver  --image_size 128  --channels 1  --GPU 0  --epoch 100000 --type train
```

Here is the list of parameters:

```
--type: 'train or test, default: train'
--project: 'the name of project, default: denoise'
--image_size: 'image size, default: 256'
--batch_size: 'batch size, default: 1'
--load_model: 'folder of saved model, default: None'
--GPU: 'GPU for running code, default: 0'
--channels: 'the channels of input image, default: 3'
--epoch: 'number of training epoch, default: 5'
```

If you broke down the training process and want to restart training, you can load the former checkpoints like this:

```
$ python main.py  --project 1_Isotropic_Liver  --image_size 128  --channels 1  --GPU 0  --epoch 100000 --type train --load_model 20190922-2222
```

You can also open tensorboard to monitor the training progress and generated images.

```
$ tensorboard --logdir 
```

## For testing

Write testing data into tfrecords

```
$ python3 build_data.py --project 1_Isotropic_Liver --type test
```

We use the same code but different parameters for training and testing and you need to load your checkpoints gained by several thousand epochs training, for example:

```
$ python main.py --epoch 500 --project 1_Isotropic_Liver --channels 1 --image_size 128 --GPU 0 --type test --load_model 20190926-1619
```

Interpretation of the above parameters:

```
--epoch:'the number of images in the testing dataset'
--load_model:'the name of checkpoint folder, you had better name it as "YYYYMMDD-HHMM" '
```

You can gain the inference images at the result folder.

## Some results

### Virtual staining

|      |      |      |      |      |
| ---- | ---- | ---- | ---- | ---- |
|      |      |      |      |      |

### Isotropic

|      |      |      |      |      |
| ---- | ---- | ---- | ---- | ---- |
|      |      |      |      |      |

### De noising

|      |      |      |      |      |
| ---- | ---- | ---- | ---- | ---- |
|      |      |      |      |      |

## Demo

## Citation and detailed manual

A paper explaining most of the effectuation details can be found here.

