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
    docs.txt からCoordinate形式の行列を作成する
    """
    
    # df_dict: Document Frequency Dictionaly
    df_dict   = {}   # 文脈頻度の辞書
    dimention = 0    # 次元数（文脈数）

    # 各単語の文脈での出現頻度を数える
    for line in open( load_name ):
        listed_line = line.rstrip().split(',')
        for term in set(listed_line):
            df_dict[term] = df_dict.get(term, 0) + 1

        # 文脈数を数え上げる
        dimention += 1

    # n個以上の文脈に出現した単語だけを保持する
    threshold = 5 
    # item[0]: 単語
    # item[1]: 頻度
    uniterms = [item[0] for item in df_dict.iteritems() \
                        if  item[1] > threshold]

    # lil_matrix形式の疎行列を生成
    lil_matrix = sparse.lil_matrix( (len(uniterms), dimention) )
    for i, term in enumerate( uniterms ):
        for j, line in enumerate( open(load_name) ):
            counts = line.rstrip().split(',').count( term )
            if counts:
                # TFの計算:文書に含まれる単語の数
                tf  = float(counts)
                # IDFの計算:log(全文書数/その単語が含まれる文書数)
                idf = math.log( float(dimention)/df_dict[term] )
                lil_matrix[i,j] = tf*idf

        print i # 進捗確認
    
    decoded_relation = map(lambda t: t.decode('utf_8'), uniterms) # decodeしないとloadmatができない
    io.savemat( save_name, {'matrix':lil_matrix, 'relation':decoded_relation} )


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    # 行列生成に使うファイルを指定できる
    if argc == 3:
        makeMatrix( load_name=argv[1], save_name=argv[2] )
    else:
        makeMatrix()
