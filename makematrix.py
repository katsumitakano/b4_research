# coding: utf-8
# 対象ファイルは docs.txt

import os
import sys
import math
import numpy as np
from scipy import io, sparse
from mylib import measure_time

@measure_time
def makeMatrix( load_name='docs.txt', save_name='matrix.mat'):
    """
    docs.txt からlil形式の疎行列を作成する
    """
    
    # df_dict: Document Frequency Dictionaly
    df_dict   = {}   # 文脈頻度の辞書
    N = 0    # 単語数
    M = 0    # 文脈数

    # 各単語の文脈での出現頻度を数える
    for line in open( load_name ):
        listed_line = line.rstrip().split(',')
        for term in set(listed_line):
            df_dict[term] = df_dict.get(term, 0) + 1

        # 文脈数を数え上げる
        M += 1

    # n個以上の文脈に出現した単語だけを保持する
    threshold = 5 
    # item[0]: 単語
    # item[1]: 頻度
    terms = [item[0] for item in df_dict.iteritems() \
                        if  item[1] > threshold]

    # 文書をリストに格納しておく（docsが100MB程度なら問題ない）
    documents = [ line.rstrip().split(',') \
                      for line in open(load_name) ]

    # lil_matrix形式の疎行列を生成
    N = len(terms)
    lil_matrix = sparse.lil_matrix( (N, M) )
    for i, term in enumerate( terms ):
        for j, line in enumerate( documents ):
            counts = line.count( term ) #TODO:countの高速化を考える（正規表現？）
            if counts:
                # TFの計算:文書に含まれる単語の数
                tf  = float(counts)
                # IDFの計算:log(全文書数/その単語が含まれる文書数)
                idf = math.log( float(M)/df_dict[term] )
                lil_matrix[i,j] = tf*idf

        print "makematrix:%d/%d" % (i, N) # 進捗確認
    
    decoded_relation = map(lambda t: t.decode('utf_8'), terms) # decodeしないとloadmatができない
    io.savemat( save_name, {'matrix':lil_matrix, 'relation':decoded_relation} )


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    # 行列生成に使うファイルを指定できる
    if argc == 3:
        makeMatrix( load_name=argv[1], save_name=argv[2] )
    else:
        makeMatrix()
