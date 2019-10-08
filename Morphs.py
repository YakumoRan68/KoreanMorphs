from __future__ import absolute_import, division, print_function, unicode_literals
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import tensorflow as tf
from tensorflow import keras
import numpy as np
from konlpy.tag import *
import os
import konlpy


class Morphs():
    def __init__(self):
        self.kkma = Kkma()
        self.komoran = Komoran()
        self.hannanum = Hannanum()

    def get_sentences(self, document):
        '문서->문장'
        return self.kkma.sentences(document)

    def get_morphs(self, sentences):
        '문장->단어'
        self.morphs = []
        self.tag = []
        
        for sentence in sentences:
            kp = self.komoran.pos(sentence)
            hp = self.hannanum.pos(sentence)

            if len(kp)!=len(hp):
                continue

            morph_buffer = []
            tag_buffer = []
            for i in range(len(kp)) :
                
                if kp[i][0] != hp[i][0] | kp[i][1][0] != hp[i][1][0] :
                    morph_buffer.clear()
                    tag_buffer.clear()
                    break
                else :
                    morph_buffer.append(kp[i][1])
                    tag_buffer.append(kp[i][1])
                    

            self.morphs.append(morph_buffer)
            self.tag.append(tag_buffer)
            

    def bow(self, words):
        '단어->숫자'
        raise

    def pos(self, document):
        '문서->형태소'
        raise

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
        
    def load(self, path):
        'load trainned model'
        raise




if __name__=='__main__':
    path = ''#path of model
    
    morphs = Morphs()
    document = konlpy.corpus.kolaw.open('constitution.txt').read()
    sentences = morphs.get_sentences(document)
    morphs.get_morphs(sentences)
