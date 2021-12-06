#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 00:03:32 2021

@author: richardzhu
"""
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from scipy import spatial
import numpy as np
# import sys
import string

# #Input files, can also you sys
# q = open(sys.argv[1], 'r').readlines()
# a = open(sys.argv[2], 'r').readlines()
q = open("cran.qry", 'r').readlines()
a = open("cran.all.1400", 'r').readlines()

lemmatizer = WordNetLemmatizer()

#Stop words
closed_class_stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',
                           'as','at','by','for','from','in','into','like','minus','near','of','off','on',
                           'onto','out','over','past','per','plus','since','till','to','under','until','up',
                           'via','vs','with','that','can','cannot','could','may','might','must',
                           'need','ought','shall','should','will','would','have','had','has','having','be',
                           'is','am','are','was','were','being','been','get','gets','got','gotten',
                           'getting','seem','seeming','seems','seemed',
                           'enough', 'both', 'all', 'your' 'those', 'this', 'these', 
                           'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',
                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',
                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',
                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',
                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',
                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',
                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',
                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', 
                           'anything', 'anytime' 'anywhere', 'everybody', 'everyday',
                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',
                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',
                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',
                           'you','your','yours','me','my','mine','I','we','us','much','and/or'
                           ]

#Queries
queries = [""]*225
index = -1
space = 1
for line in q:
    if line[0:2] == '.I':
        index += 1
        space = 0
    elif line[0:2] != '.W':
        if not space:
            queries[index]+=line[:len(line)-1]
            space = 1
        else: queries[index]+=" "+line[:len(line)-1]
        
for i in range(len(queries)):
    queries[i] = queries[i].translate(str.maketrans('', '', string.punctuation))
    queries[i] = queries[i].translate(str.maketrans('', '', string.digits))
    queries[i] = word_tokenize(queries[i])
    queries[i] = [word for word in queries[i] if not word in closed_class_stop_words]
    
# for i in range(len(queries)):
#     for j in range(len(queries[i])):
#         word = queries[i][j]
#         if word[len(word)-1]=='s':queries[i][j] = word[0:len(word)-1]
#         elif word[len(word)-2:len(word)]=='es':queries[i][j] = word[0:len(word)-2]
#         elif word[len(word)-3:len(word)]=='ing':queries[i][j] = word[0:len(word)-3]
   
freqDistQ = {}
for query in queries:
    counted = []
    for word in query:
        if word not in counted:
            if word not in freqDistQ:
                freqDistQ[word]=1
            else: freqDistQ[word]+=1
            counted.append(word)
            
queryTFIDF = {}          
for i in range(len(queries)):
    queryTFIDF[i] = {}
    for j in range(len(queries[i])):
        termFrequency = np.log(queries[i].count(queries[i][j])/len(queries[i]))
        appearances = 0 
        IDF = np.log(len(queries)/freqDistQ[queries[i][j]])
        queryTFIDF[i][queries[i][j]] = termFrequency*IDF
    
#Abstracts        
abstracts = [""]*1400
index = -1
space = 1
add = 0
for line in a:
    if line[0:2] == '.I':
        index += 1
        add = 0
        space = 0
    elif line[0:2] == '.W':
        add = 1
    elif add:
        if not space:
            abstracts[index]+=line[:len(line)-1]
            space = 1
        else: abstracts[index]+=" "+line[:len(line)-1]
        
for i in range(len(abstracts)):
    abstracts[i] = abstracts[i].translate(str.maketrans('', '', string.punctuation))
    abstracts[i] = abstracts[i].translate(str.maketrans('', '', string.digits))
    abstracts[i] = word_tokenize(abstracts[i])
    abstracts[i] = [word for word in abstracts[i] if not word in closed_class_stop_words]

# for i in range(len(abstracts)):
#     for j in range(len(abstracts[i])):
#         word = abstracts[i][j]
#         if word[len(word)-1]=='s':abstracts[i][j] = word[0:len(word)-1]
#         elif word[len(word)-2:len(word)]=='es':abstracts[i][j] = word[0:len(word)-2]
#         elif word[len(word)-3:len(word)]=='ing':abstracts[i][j] = word[0:len(word)-3]

freqDistA = {}
for abstract in abstracts:
    counted = []
    for word in abstract:
        if word not in counted:
            if word not in freqDistA:
                freqDistA[word]=1
            else: freqDistA[word]+=1
            counted.append(word)
       
abstractTFIDF = {}         
for i in range(len(abstracts)):
    abstractTFIDF[i] = {}
    for j in range(len(abstracts[i])):
        termFrequency = np.log(abstracts[i].count(abstracts[i][j])/len(abstracts[i]))
        appearances = 1
        IDF = np.log(len(abstracts)/freqDistA[abstracts[i][j]])
        if abstracts[i][j] not in abstractTFIDF[i]:
            abstractTFIDF[i][abstracts[i][j]] = termFrequency*IDF
            
#IR
cosineSimilarity = {}
for i in range(len(queries)):
    cosineSimilarity[i] = {}
    for j in range(len(abstracts)):
        queryVector = []
        abstractVector = []
        zero = 1
        for word in queries[i]:
            if word in abstracts[j]:
                abstractVector.append(abstractTFIDF[j][word])
                zero = 0
            else:
                abstractVector.append(0)
            queryVector.append(queryTFIDF[i][word])
        if zero: None #eliminate items with score 0
        else: cosineSimilarity[i][j]=1 - spatial.distance.cosine(queryVector, abstractVector)

#Sort by cosine similarity
for i in range(len(cosineSimilarity)):
    cosineSimilarity[i] = dict(sorted(cosineSimilarity[i].items(), key=lambda item: item[1], reverse=True))

#Output
output = open("output.txt", "w")
for i in range(len(cosineSimilarity)):
    l = list(cosineSimilarity[i])
    for j in range(len(cosineSimilarity[i])):
        output.write(str(i+1) + " " + str(l[j]+1) + " " + str(cosineSimilarity[i][l[j]]))
        output.write("\n")