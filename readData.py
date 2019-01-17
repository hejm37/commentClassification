import csv
import re
import jieba
import gensim
import numpy as np
from random import shuffle
from dataDir.utils import remove_noise

def readFromFile(filename):
    dataLines = []
    with open(filename, newline='',encoding='utf-8') as f:
#         去除第一行
        f.readline()
        rows = csv.reader(f)
        dataLines = list(rows)
#         将字符型label转换为整数型label，并且补全将‘’补成0
        for dataLine in dataLines:
            if dataLine[1] == '0.0' or dataLine[1] == '':
                dataLine[1] = 0
            elif dataLine[1] == '1.0':
                dataLine[1] = 1
        
#         如果数据被标记为模版，则同时标记为水评
            if dataLine[0] == '0.0' or dataLine[0] == '':
                dataLine[0] = 0
            elif dataLine[0] == '1.0':
                dataLine[0] = 1
                dataLine[1] = 1
    return dataLines

def segmentation(text):
    return jieba.cut(text)

def loadStopWords(filename):
    stopwords = [line.strip() for line in \
                 open(filename, 'r', encoding='utf-8').readlines()]
    return stopwords

def readTaobaoData():
    filenames = ['data/part1.csv', 'data/part2.csv', 'data/part4.csv',
                'data/template1.csv','data/template2.csv']
    dataLines = []
    for filename in filenames:
        dataLines_ = readFromFile(filename)
        dataLines += dataLines_

    # comment data preprocessing
    ## 0. shuffle data
    shuffle(dataLines)

    ## 1. remove default comment
    dataLines1 = [line for line in dataLines if line[2] != '此用户没有填写评论!']

    ## 2. remove noise
    ## [参考](https://blog.csdn.net/mach_learn/article/details/41744487)
    dataLines2 = [[line[0], line[1], remove_noise(line[2])] for line in dataLines1]

    ## 3. text segmentation
    dataLines3 = [[line[0], line[1], segmentation(line[2])] for line in dataLines2]

    ## 4. remove stop words
    stopWordFilename = 'data/stop_words.txt'
    stopWords = loadStopWords(stopWordFilename)
    dataLines4 = [[line[0], line[1], 
                   [word for word in line[2] if word not in stopWords]]
                  for line in dataLines3]

    ## 5. word Embedding, the word2Vec training see folder word2vec
    model = gensim.models.Word2Vec.load('word2vec/w2v.model')
    dataLines5 = []
    for line in dataLines4:
        words = []
        words = [model.wv[word] for word in line[2] if word in list(model.wv.vocab)]
        # 如果去除停用词后，暂且将其词向量表示设为全0
        if len(words) == 0:
            wordsVec = [0 for i in range(100)]
        else:
            wordsVec = sum(words)
        dataLines5.append([line[0], line[1], wordsVec])

    return dataLines5, dataLines
