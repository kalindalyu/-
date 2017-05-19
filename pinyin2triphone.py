#!/usr/bin/python 
# -*- coding: utf-8 -*- 
"""
created on May 14th
@ author:  Lyu Tongtong 
"""

from collections import OrderedDict
import os,sys,string

 
# sentence = 'wo3 ai4 bei3 jing1 tian1 an1 men2'
initialList = ['b','p','m','f','z','s','c','d','t','n','l','zh', 'ch','sh','r', \
'zh', 'ch','sh','r','j','q','x','g','k','h']
finalList = ['a', 'ia', 'ua', 'e','ie','ve','ai','ei','uai','ui','i','Qi','Pi', \
'v','u','ou','iu','ao','iao','o','uo','er','iang','ing','uang','ong','eng','ang','iong', \
'ian', 'in', 'uan', 'un', 'en', 'an', 'van','vn','uen','ueng']
class_initial_bilabial = ['b','p','m'] #B 
class_initial_k_dental = ['f'] #F
class_initial_dental = ['z','s','c'] #Z
class_initial_alveolar = ['d','t','n','l'] #D
class_initial_retroflex = ['zh', 'ch','sh','r'] #QZ
class_initial_palatar = ['j','q','x'] #Q
class_initial_valar = ['g','k','h'] #K

# finalList 
class_final_mono = ['a','o','e','i','u','v','er','Qi','Pi']
class_final_compound = ['ai', 'ei', 'ao','ou','ia','ie','ua','uo','ve','iao','iou','uai','uei']
class_final_nasal = ['an','ian','uan','van','en','in','uen','vn','ang', \
'iang','uang','eng','ing','ueng','ong','iong']

def read_file_list(file_name):
    source_corpus_List = []
    fid = open(file_name)
    for line in fid.readlines():
        line = line.strip()
        if len(line) < 1:
            continue
        else:
            source_corpus_List.append(line)
    fid.close()
    return source_corpus_List

def loadDict(syfile):
    syDict = OrderedDict()
    with open(syfile, 'r') as f: 
        for line in f: 
            sy = line.strip().split()
            key = sy[0] 
            value = sy[1:]
            syDict[key] = value
    return syDict 

def pinyin2syllable(pinyin,phonemeList,toneList,syDict):
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
        ## punctuation -> pau0 
        phonemeList.append(sys)
        toneList.append(tone)          
    return phonemeList, toneList

def phoneme2segment(sentence,syDict):
    ## sil at the head of sentence 
    phonemeList = []
    toneList = []
    trans_phonemeList = []
    trans_phonemeList.append('nil')
    toneList.append('nil')
    for ph in sentence.split(): 
        phonemeList, toneList = pinyin2syllable(ph,phonemeList,toneList,syDict) 

    for sy_with_tone in phonemeList: 
        sy_without_tone = sy_with_tone[:-1]
        if sy_without_tone in class_initial_bilabial:
            trans_phonemeList.append('B')
        elif sy_without_tone in class_initial_k_dental:
            trans_phonemeList.append('F')
        elif sy_without_tone in class_initial_dental:
            trans_phonemeList.append('Z')
        elif sy_without_tone in class_initial_alveolar:
            trans_phonemeList.append('D')
        elif sy_without_tone in class_initial_retroflex:
            trans_phonemeList.append('R') 
        elif sy_without_tone in class_initial_palatar:
            trans_phonemeList.append('Q')
        elif sy_without_tone in class_initial_valar:
            trans_phonemeList.append('K')
        elif sy_without_tone in class_final_mono:
            trans_phonemeList.append('M')
        elif sy_without_tone in class_final_compound:
            trans_phonemeList.append('C')
        elif sy_without_tone in class_final_nasal:
            trans_phonemeList.append('N')
    # sil in the end of sentence
    trans_phonemeList.append('nil')
    toneList.append('nil')  
    return  trans_phonemeList,toneList

# create features of one sentence 
def create_one_sentence_features(trans_phonemeList, toneList):
    index = 1
    triple_mono_List = []
    
    for i in range(len(trans_phonemeList)):
        '''
        Four factors are considered in this scripts
        factor 1: Identity of the previous syllable
        factor 2: Identity of the previous tone
        factor 3: Identity of the next syllable
        factor 4: Identity of the next tone
        '''
        if i < len(trans_phonemeList) - 2:
            tuple = trans_phonemeList[i+1] + '-' + toneList[i+1] # the information of current syllable and its tone 
            #print tuple
            # factor 1 
            triple_pre_sy = tuple + '-' + trans_phonemeList[i]
            # factor 2
            triple_next_sy = tuple + '-' + trans_phonemeList[i+2]
            # factor 3
            triple_pre_tone = tuple + '-' + toneList[i]
            # factor 4
            triple_next_tone = tuple + '-' + toneList[i+2]
            triple_mono_List.append(triple_pre_sy)
            triple_mono_List.append(triple_pre_tone)
            triple_mono_List.append(triple_next_sy)
            triple_mono_List.append(triple_next_tone)
        else:
            exit
    return triple_mono_List

def create_full_features(source_corpus_List): ## calculate uniq triples and their numbers 
    triple_full_List = []
    for sentence in source_corpus_List:
        trans_phonemeList,toneList = phoneme2segment(sentence,syDict)
        triple_mono_List = create_one_sentence_features(trans_phonemeList, toneList)
        for triple in triple_mono_List:
            if triple not in triple_full_List:
                triple_full_List.append(triple)
            else:
                pass 
                '''
            if triple not in triple_mono_List:
                triple_full_dict[triple] = 1 
            else:
                triple_full_dict[triple] += 1 
            '''
    return triple_full_List

def greedy_selection(source_corpus_List,target_corpus_List,triple_target_List):
    sentence_score_dict = {}
    for sentence in source_corpus_List:
        trans_phonemeList,toneList = phoneme2segment(sentence,syDict)
        triple_mono_List = create_one_sentence_features(trans_phonemeList, toneList)
        L = len(triple_mono_List) # the number of triples in one sentence 
        triple_new_mono_List = []
        #print triple_target_List
        for triple in triple_mono_List: 
            if triple not in triple_target_List:
                triple_new_mono_List.append(triple)
            else:
                pass
        triple_target_List.extend(triple_new_mono_List)
        #print triple_target_List
         # K is the number of new units in the sentence acccording to the target corpus
        K = len(triple_new_mono_List) 
        print  L,K
        p = float(K)/float(L) ##
        sentence_score_dict[sentence] = p 
    print sentence_score_dict
    best_sentence = max(sentence_score_dict, key=sentence_score_dict.get) 
    print best_sentence
    source_corpus_List.remove(best_sentence)
    target_corpus_List.append(best_sentence)

    return source_corpus_List, target_corpus_List, triple_target_List


syDict = loadDict('syd.dict')
source_corpus_List = read_file_list('sentence.txt')

triple_full_List = create_full_features(source_corpus_List)
target_corpus_List = []
triple_target_List = []

while (len(triple_target_List) != len(triple_full_List)):
    source_corpus_List, target_corpus_List, triple_target_List = greedy_selection(source_corpus_List,target_corpus_List,triple_target_List)


    








                                                                                                                                                                                                                                                                                                                                                                                                                                                             




    
        

    
