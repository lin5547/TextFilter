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


def filter_other(line):
    """
    filter out characters that are not Chinese, letters, normal punctuations or numbers.
    """


    if len(line) > 0:
        for uchar in line:
            if not is_chinese(uchar):
                line = line.replace(uchar, u'')


    return line

def filteAlpha(line):
    return re.sub("[a-zA-Z]".decode('utf-8'),'',line)

def filtePun(line,string):

    return re.sub("[\s+\´•.\!\/_,?$%^*(+:;\"\'=★]+|[+——！，。？、~@#￥%……&*（）；：=]+".decode("utf8"), string.decode("utf8"),line)

def filter_brackets(line):
    """
    Filter out words, especailly emoticon phrases, that are surrounded by square
    brackets.
    """
    a1 = re.compile(r'[［[].*?[]］]' )
    a2 = re.compile(r'[〈〉.*?〈〉]'.decode('utf-8'))
    a3 = re.compile(r'[【】.*?【】]'.decode('utf-8'))
    line = a1.sub('', line)
    line = a2.sub('',line)
    line = a3.sub('',line)
    return line
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

