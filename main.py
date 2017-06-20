#coding=utf-8
import argparse
import json
import codecs
import process_text as pt
from tqdm import tqdm
import jieba
def _str_to_bool(s):
    """Convert string to bool (in argparse context)."""
    if s.lower() not in ['true', 'false']:
        raise ValueError('Argument needs to be a '
                         'boolean, got {}'.format(s))
    return {'true': True, 'false': False}[s.lower()]

def main():
    parser = argparse.ArgumentParser(
        description='Text filter'
    )
    parser.add_argument('--pun',type=_str_to_bool,default=True,help='去掉所有标点符号')
    parser.add_argument('--space',type=_str_to_bool,default=True,help='合并连续空格')
    parser.add_argument('--q2b',type=_str_to_bool,default=True,help='全角转半角')
    parser.add_argument('--t2s',type=_str_to_bool,default=True,help='繁体转简体')
    parser.add_argument('--dig',type=_str_to_bool,default=True,help='数字过滤')
    parser.add_argument('--url', type=_str_to_bool, default=True, help='网址过滤')
    parser.add_argument('--noC', type=_str_to_bool, default=True, help='非中文过滤')
    parser.add_argument('--bra', type=_str_to_bool, default=True, help='过滤【】里面的内容')
    parser.add_argument('--alpha', type=_str_to_bool, default=True, help='过滤英文字符')
    parser.add_argument('--seg', type=_str_to_bool, default=True, help='分词处理')
    parser.add_argument('--i', type=str, default=None, help='输入文件')
    parser.add_argument('--o', type=str, default=None, help='输出文件')
    args = parser.parse_args()
    print(json.dumps(args.__dict__))

    with codecs.open(args.i,mode='r',encoding='utf-8') as fin:
        sentences = fin.readlines()

    f = codecs.open(args.o,'w','utf-8')

    for i in tqdm(range(len(sentences))):
        line = sentences[i]
        line=line.strip('\n').strip('\r').strip('\r\n').strip('\n\r')

        if line=='':
            f.write('\n')
            continue
        if args.bra:
            line = pt.filter_brackets(line)
        if args.alpha:
            line = pt.filteAlpha(line)
        if args.q2b:
            line = pt.strQ2B(line)
        if args.space:
            line = pt.spaceFilter(line,' ')
        if args.url:
            line = pt.urlFilter(line,'')
        if args.dig:
            line = pt.digitFilter(line,'')
        if args.pun:
            line = pt.filtePun(line,'')
        if args.noC:
            line = pt.filter_other(line)
        if args.t2s:
            line = pt.tradition2simple(line)
        if args.seg:
            line = ' '.join(jieba.cut(line))
        if line=='':
            continue
        f.write(line+'\n')

    f.close()

if __name__=='__main__':
    main()
