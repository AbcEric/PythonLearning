import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from keras import backend as K

num_classes = 10
img_rows, img_cols = 28, 28

(trainX, trainY), (testX, testY) = mnist.load_data()