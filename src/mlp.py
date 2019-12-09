from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from random import shuffle
import random
import tensorflow as tf
import numpy as np
import os
import datetime
from sql import *
from sklearn.model_selection import train_test_split



#tag to vector
def one_hot(tag):
    one_hot = []
    for c in 'NVMJESX':
        one_hot.append(1 if c==tag else 0)
    return one_hot

#random set for test
def random_set():
    x_data = [i for i in range(1000)]
    y_data = [one_hot(tags[int(random.random()*7)]) for i in range(1000)]

    return (x_data[:700], y_data[:700]), (x_data[700:], y_data[700:])

#prepare dataset
def prepare():
    data = show_data('dictionary', 'Words')

    x_data = []
    y_data = []

    shuffle(data)

    for d in data:
        x_data.append([d[0], 0 if d[3]=='' else int(d[3]), 0 if d[4]=='' else int(d[4])])
        y_data.append(one_hot(d[2]))

    return train_test_split(x_data, y_data, test_size=0.2)

#training model
def train(x_train, y_train, x_test, y_test):
    #layers
    model = Sequential()
    model.add(Dense(64, activation='relu', input_dim=3))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(7, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    #log를 기록할 경로
    log_dir = os.path.join(
        "logs",
        "fit",
        datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),
    )
    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

    #training
    model.fit(x_train, y_train,
              epochs=10,
              validation_data=(x_test, y_test), 
              callbacks=[tensorboard_callback])
    model.save(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

def load_model(m):
    return keras.models.load_model(m)

    

#tensorboard 사용(기본경로 바탕화면/src)
def use_tensorboard():
    os.system('explorer http://localhost:6006')
    os.system('tensorboard --logdir %systemdrive%/users/%username%/desktop/src/logs/fit')
