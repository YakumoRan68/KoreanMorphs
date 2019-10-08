from __future__ import absolute_import, division, print_function, unicode_literals
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import tensorflow as tf
from tensorflow import keras
import numpy as np
import konlpy
from konlpy.tag import *
import os
import gensim

class Morphs():
    def __init__(self):
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
                    print(step, sess.run(cost, feed_dict={X : x_data, Y:y_data}))
                    #print(sess.run(tf.arg_max(result,1)))
                    print(result)

    def 
                    




if __name__=='__main__':
    a = Morphs()
