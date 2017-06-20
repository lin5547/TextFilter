#! /usr/bin/env python2.7
#coding=utf-8

from langconv import *
import re
import codecs
import os
from os import path
from gensim.models import word2vec
import pandas as pd
from nltk.probability import FreqDist
import numpy as np

import nltk


def filtePun(line,string):
    return re.sub("[\s+\.\!\/_,?$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), string.decode("utf8"),line)
# 读单个文本
def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += unichr(inside_code)
    return rstring

# 将数字用digtal代替
def digitFilter(contents,string):
    digitPattern = re.compile('\d+\.?\d*')
    contents = re.sub(digitPattern, string, contents)
    return contents
# 简体转繁体
def simple2tradition(line):
    # 将简体转换成繁体
    line = Converter('zh-hant').convert(line.decode('utf-8'))
    # line = line.encode('utf-8')
    return line

# 繁体转简体
def tradition2simple(line):
    # 将繁体转换成简体
    line = Converter('zh-hans').convert(line)
    # line = line.encode('utf-8')
    return line
#判断字符uchar是否为汉字
def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

# 将网址用URL代替
def urlFilter(contents,string):
    urlPattern = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    contents = re.sub(urlPattern, string, contents)  # 将网址用URL代替
    # print 'url filtering', contents
    return contents

#将多个连续空格用一个空格代替
def spaceFilter(contents,string):
    contents = re.sub('\s+', string, contents)  # 将
    return contents
# 读单个文本

def load_file(input_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    input_text = input_data.read()
    return input_text


# 读取目录下文本成为一个字符串
def load_dir(input_dir):
    # files = list_dir(input_dir)
    files = os.listdir(input_dir)
    seg_files_path = [path.join(input_dir, f) for f in files]
    output = []
    for txt in seg_files_path:
        output.append(load_file(txt))
    return '\n'.join(output)

#合并多个目录下的文本
def load_txt(x):
    with open(x) as f:
        #res = [t for t in f]
        res = [t.decode('gbk','ignore') for t in f]#.decode('gbk','ignore')
        return ''.join(res)
def compose_dir(rootdir,outfile):
    # rootdir = 'posdata/traindata/2014/'
    # print(rootdir)
    dirs = os.listdir(rootdir)
    dirs = [path.join(rootdir,f) for f in dirs]#将目录下以C开头的文件夹添加进目录
    #dirs = [path.join(rootdir,f) for f in dirs ]
    text_t = {}
    num=0
    #enumerat遍历索引和遍历元素
    for i, d in enumerate(dirs):
        files = os.listdir(d)#dirs内的子文件夹名数组
        files = [path.join(d, x) for x in files if x.endswith('txt') and not x.startswith('.')]#将每个子文件夹中的.txt文件添加进路径
        text_t[i] = [load_txt(f) for f in files ]
        num=num+1
    print("num",num)
    #保存为一个文本
    # outfile='posdata/traindata/2014_training.utf8'
    outdata = codecs.open(outfile, 'w', 'utf-8')
    for i in xrange(num):
        for sentence in text_t[i]:
            outdata.write(sentence)
    outdata.close()
# nltk  输入文本，输出词频表
def freq_func(input_txt):
    corpus = nltk.Text(input_txt)
    fdist = FreqDist(corpus)
    w = fdist.keys()
    v = fdist.values()
    freqdf = pd.DataFrame({'word': w, 'freq': v})
    freqdf.sort('freq', ascending=False, inplace=True)
    freqdf['idx'] = np.arange(len(v))
    return freqdf

# word2vec建模
def trainW2V(corpus, epochs=10, num_features=50, sg=1, \
             min_word_count=1, num_workers=4, \
             context=4, sample=1e-5, negative=5):
    w2v = word2vec.Word2Vec(workers=num_workers,
                            sample=sample,
                            size=num_features,
                            min_count=min_word_count,
                            window=context)
    #np.random.shuffle(corpus)
    w2v.build_vocab(corpus)
    for epoch in range(epochs):
        print('epoch' + str(epoch))
        #np.random.shuffle(corpus)
        w2v.train(corpus)#训练
        w2v.alpha *= 0.9#更新学习率
        w2v.min_alpha = w2v.alpha
    print("word2vec DONE.")
    return w2v
def save_w2v(w2v, idx2word):
    # 保存词向量lookup矩阵，按idx位置存放
    init_weight_wv = []
    for i in range(len(idx2word)):
        init_weight_wv.append(w2v[idx2word[i]])
    return init_weight_wv

# word2vec训练
def train_vec(txtwv,epoch=1,num_features=50,savepath=None):
    sentences = []
    for line in txtwv:
        sentences.append(line.strip('\n').split(' '))
    w2v = trainW2V(sentences,epochs=epoch,num_features=num_features)
    w2v.save(savepath)#保存训练好的词向量模型



def creat_dict(filename):
    input_text = load_file(filename) # 读入全部文本
    txtwv = [line.split() for line in input_text.split('\n') if line != '']  # 为词向量准备的文本格式
    txtnltk = [w for w in input_text.split()]   # 为计算词频准备的文本格式
    freqdf = freq_func(txtnltk) # 计算词频表
    maxword = freqdf.shape[0] # 词汇个数
    #  建立两个映射字典
    word2idx = dict((c, i) for c, i in zip(freqdf.word, freqdf.idx))
    idx2word = dict((i, c) for c, i in zip(freqdf.word, freqdf.idx))
    return word2idx
