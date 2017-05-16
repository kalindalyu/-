#!/usr/bin/python 
# -*- coding: utf-8 -*- 
"""
created on May 14th
@ author:  Lyu Tongtong 
"""

from collections import OrderedDict
import os,sys,string


sentence = 'wo3 ai4 bei3 jing1 tian1 an1 men2'
initialList = ['b','p','m','f','z','s','c','d','t','n','l','zh', 'ch','sh','r', \
'zh', 'ch','sh','r','j','q','x','g','k','h']
finalList = ['a', 'ia', 'ua', 'e','ie','ve','ai','ei','uai','ui','i','Qi','Pi', \
'v','u','ou','iu','ao','iao','o','uo','er','iang','ing','uang','ong','eng','ang','iong', \
'ian', 'in', 'uan', 'un', 'en', 'an', 'van','vn','uen','ueng']
class_initial_bilabial = ['b','p','m']
class_initial_k_dental = ['f']
class_initial_dental = ['z','s','c']
class_initial_alveolar = ['d','t','n','l']
class_initial_retroflex = ['zh', 'ch','sh','r']
class_initial_palatar = ['j','q','x']
class_initial_valar = ['g','k','h']

# finalList 
class_final_A = ['a', 'ia', 'ua']
class_final_E = ['e','ie','ve']
class_final_I1 = ['ai','ei','uai','ui']
class_final_I2 = ['i','Qi','Pi']
class_final_V = ['v']
class_final_U = ['u','ou','iu','ao','iao']
class_final_O = ['o','uo']
class_final_R = ['er']
class_final_G = ['iang','ing','uang','ong','eng','ang','iong']
class_final_N = ['ian', 'in', 'uan', 'un', 'en', 'an', 'van','vn','uen','ueng']




def loadDict(syfile):
    syDict = OrderedDict()
    with open(syfile, 'r') as f: 
        for line in f: 
            sy = line.strip().split()
            key = sy[0] 
            value = sy[1:]
            syDict[key] = value
    return syDict 

def pinyin2phoneme(pinyin,phonemeList,syDict):
    print pinyin
    tone = pinyin[-1]
    syList = syDict.get(pinyin)
    sy_newList = []
    for sy in syList:
        if sy[-1] not in '012345':
            sy_new = sy + tone
            sy_newList.append(sy_new)
        else:
            sy_newList.append(sy)
    for sys in sy_newList:
        #sy = filter(lambda ch: ch not in '012345', sy)
        phonemeList.append(sys)
    return phonemeList

## test 
syDict = loadDict('syd.dict')
phonemeList = []

for ph in sentence.split(): 
    syList = pinyin2phoneme(ph,phonemeList, syDict) 


# pinyin_coversion 




    
        

    
