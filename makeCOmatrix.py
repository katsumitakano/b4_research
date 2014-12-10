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
def makeCOMatrix( threshold=10 ):
    """
    docs.txt からlil形式の疎行列を作成する
    """
    load_name='docs.txt'
    save_name='matrix_co.mat'
    
    # df_dict: Document Frequency Dictionaly
    df_dict = {} # 文脈頻度の辞書
    N = 0        # 単語数

    # 文書をリストに格納しておく（docsが100MB程度なら問題ない）
    documents = [ line.rstrip().split(',') \
                      for line in open(load_name) ]
    
    # 各単語の文脈での出現頻度を数える
    for line in documents:
        for term in set(line):
            df_dict[term] = df_dict.get(term, 0) + 1

    # item[0]: 単語
    # item[1]: 頻度
    terms = [item[0] for item in df_dict.iteritems() \
                        if  item[1] > threshold]

    # lil_matrix形式の疎行列を生成
    N = len(terms)
    lil_matrix = sparse.lil_matrix( (N, N) )
    for i, term in enumerate( terms ):
        for _, line in enumerate( documents ):
            # 文書に単語が含まれていない
            if line.count( term ) == 0: continue

            # 共起頻度を数え上げる
            for t in set(line):
                try:    idx = terms.index(t)
                except: continue
                lil_matrix[i,idx] += 1

        print "makeCOmatrix:%d/%d" % (i, N) # 進捗確認
    
    # 相互情報量による重み付け
    weight_matrix = sparse.lil_matrix( (N, N) )
    sum_all  = lil_matrix.sum()
    sum_axis = np.array( lil_matrix.sum(axis=0) )[0] # 各列の和
    for i in xrange(N):
        for j in xrange(N):
            ptc = lil_matrix[i,j]
            if ptc == 0: continue # 要素が0の時は計算しない
            pt1 = sum_axis[i]
            pt2 = sum_axis[j]
            ans = ( sum_all*ptc )/( pt1*pt2 )
            pmi = math.log(ans, 2)
            weight_matrix[i,j] = pmi

        print "weight_pmi:%d/%d" % (i, N) # 進捗確認

    # mat形式で保存 (decodeしないとloadmatができない)
    decoded_terms = map(lambda t: t.decode('utf_8'), terms)
    io.savemat( save_name, {'matrix':weight_matrix, 'terms':decoded_terms} )

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
        makeCOMatrix( threshold=int(argv[1]) )
    else:
        makeCOMatrix()
