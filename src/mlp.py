from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
#from tensorflow.keras.optimizers import SGD
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

    #예비 optimizer sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
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
              epochs=20,
              validation_data=(x_test, y_test), 
              callbacks=[tensorboard_callback])

#tensorboard 사용(기본경로 바탕화면/src)
def use_tensorboard():
    os.system('explorer http://localhost:6006')
    os.system('tensorboard --logdir %systemdrive%/users/%username%/desktop/src/logs/fit')




#for test (another model)
'''
x_train = np.random.random((1000, 20))
y_train = keras.utils.to_categorical(np.random.randint(10, size=(1000, 1)), num_classes=10)
x_test = np.random.random((100, 20))
y_test = keras.utils.to_categorical(np.random.randint(10, size=(100, 1)), num_classes=10)
num_words = 20


model = keras.models.Sequential([
    keras.layers.Dense(16, activation='relu', input_shape=(num_words,)),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(1, activation='softmax')
])


model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

log_dir = os.path.join(
    "logs",
    "fit",
    datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),
)
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

model.fit(x=x_train, 
          y=y_train, 
          epochs=5,
          validation_data=(x_test, y_test), 
          callbacks=[tensorboard_callback])



#tensorflow
def train(self):
        'model trainning'
        x_data = [] #format : [word]
        y_data = [] #format : [morpheme]
                
        
        
        X = tf.placeholder(tf.float32, [None, 3])
        Y = tf.placeholder(tf.float32, [None, 7])
        classes = 7

        W = tf.Variable(tf.random_normal([3, classes]), name='weight')
        b = tf.Variable(tf.random_normal([classes]), name='bias')

        hypothesis = tf.nn.softmax(tf.matmul(X, W) + b)
        cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(hypothesis), axis=1))

        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost)

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            for step in range(2001):
                result = sess.run(optimizer, feed_dict={X : x_data, Y : y_data})
                if step % 200 == 00:
                    print(step, sess.run(cost, feed_dict={X : x_data, Y : y_data}))
                    #print(sess.run(tf.arg_max(result,1)))
                    print(result)
'''
