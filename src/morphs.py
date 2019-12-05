#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import warnings
warnings.simplefilter('ignore', FutureWarning)
warnings.simplefilter("ignore", UserWarning)
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
        self.okt = Okt()
        
        self.morphs = []
        self.tags = []
        
        self.bag = {}

    def get_sentences(self, document):
        '문서->문장'
        print('parsing document to senteces')
        return self.kkma.sentences(document)

    def get_morphs(self, sentences):
        '문장->단어'
        
        print('getting morphs from sentences')
        for sentence in sentences:
            kop = self.komoran.pos(sentence)
            kkp = self.kkma.pos(sentence)
            hp = self.hannanum.pos(sentence)
            op = self.okt.pos(sentence)
            pos = ((kop, kkp), (kkp, hp), (hp, op), (kop, op), (kop, hp), (kkp, op))

            for p in pos:
                if len(p[0])!=len(p[1]):
                    continue
            
                morph_buffer = []
                tag_buffer = []
                for i in range(len(p[0])) :
                    if ((p[0][i][0] == p[1][i][0]) & (p[0][i][1][0] == p[1][i][1][0])):
                        morph_buffer.append(p[0][i][0])
                        tag_buffer.append(p[0][i][1][0])
                    else :
                        morph_buffer.clear()
                        tag_buffer.clear()
                        break
                        
                        
                if len(tag_buffer):
                    self.morphs.append(morph_buffer)
                    self.tags.append(tag_buffer)
            

    def pos(self, document):
        '문서->형태소'
        print('parsing...')
        sentences = self.get_sentences(document)
        self.get_morphs(sentences)
        print('done')

    
        
    def load(self, path):
        'load trainned model'
        raise


    


#test
'''
if __name__=='__main__':   
    morphs = Morphs()
    document = konlpy.corpus.kolaw.open('constitution.txt').read()
    morphs.pos(document)
'''
