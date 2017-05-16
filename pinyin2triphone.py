#!/usr/bin/python 
# -*- coding: utf-8 -*- 
"""
created on May 14th
@ author:  Lyu Tongtong 
"""

from collections import OrderedDict
import os,sys,string


sentence = 'wo3 ai4 bei3 jing1 tian1 an1 men2'
class_initial_bilabial = ['b','p', 'm']




def loadDict(syfile):
    syDict = OrderedDict()
    with open(syfile, 'r') as f: 
        for line in f: 
            sy = line.strip().split()
            key = sy[0] 
            print key
            value = sy[1:]
            syDict[key] = value
    return syDict 

def pinyin2phoneme(pinyin, phonemeList ,syDict):
    print pinyin
    syList = syDict.get(pinyin)
    for sy in syList:
        sy = filter(lambda ch: ch not in '012345', sy)
        phonemeList.append(sy)
    return phonemeList

## test 
syDict = loadDict('syd.dict')
phonemeList = []

for ph in sentence.split(): 
    syList = pinyin2phoneme(ph,phonemeList, syDict) 
#print syList




    
        

    
