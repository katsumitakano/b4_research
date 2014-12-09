# coding: utf-8
# 対象ファイルは docs.txt

import os
import sys
import math
import codecs
import numpy as np
from scipy import io, sparse
from mylib import measure_time

@measure_time
def makeTFMatrix( threshold=10 ):
    """
    docs.txt からlil形式の疎行列を作成する
    """
    load_name='docs.txt'
    save_name='matrix_tf.mat'
    
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

        print "makeTFmatrix:%d/%d" % (i, N) # 進捗確認
    
    # mat形式で保存 (decodeしないとloadmatができない)
    decoded_terms = map(lambda t: t.decode('utf_8'), terms)
    io.savemat( save_name, {'matrix':lil_matrix, 'terms':decoded_terms} )

    # 全単語をファイルに書き出しておく
    with codecs.open("terms.txt", 'w', "utf-8") as f:
        # 改行文字を付与
        decoded_terms = [term + "\n" for term in decoded_terms]
        f.writelines(decoded_terms)


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    # 最低単語数を指定
    if argc == 2:
        makeTFMatrix( threshold=int(argv[1]) )
    else:
        makeTFMatrix()
