#! /usr/bin/env python2.7
# - *- coding: utf- 8 - *-
from process_text import *
import argparse
from gensim.models import word2vec



def Q2B(filename):
    f = open(filename)
    lines = f.readlines()
    for line in lines:
        line  ='331|**|你们为什么要用繁体字呢 大企業人重要，草根創業對人力資源也是同樣的考驗和訴求|**|0'



        line = line.decode('utf-8')
        line = tradition2simple(line)
        line = strQ2B(line)
        line = re.split('[|**|]', line)
        a = line


def get_arguments():
    parser = argparse.ArgumentParser(description='sentence taging')
    parser.add_argument("--tag",type=bool,default=False,help="for taging")
    parser.add_argument("--train",type=bool,default=True,help="train taging model")
    parser.add_argument("--input",type=str,default=None,help="text files dir")
    parser.add_argument("--save_model_dir",type=str,default=None,help="the dir for saving trained model")
    parser.add_argument("--output",type=str,default=None,help="tagging result file")
    return parser.parse_args()

def train(traindata):
    train_vec(traindata)

def taging(sentence):

    return 0
def main():
    args=get_arguments()



    if args.train:
        #w2v = word2vec.Word2Vec.load('w2v_model_mixedtrain')  # 加载词向量
        #compose_dir('../dataset/SogouC.reduced/Reduced', '../dataset/sogou.txt')
        Q2B('../dataset/data.txt')

        res = [t for t in f]
        print("Q2B")
        res=strQ2B(res)
        print("tra2sim")
        res=tradition2simple(res)
        res=spaceFilter(res)
        res=urlFilter(res)
        #res = re.split('',res)
        print("train")
        train(res)
    elif args.tag:
        taging()


if __name__ == '__main__':
    main()