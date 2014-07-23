# coding: utf-8
# 対象ファイルは docs.txt

import os
import sys
import numpy as np
from scipy import io, sparse
from mylib import measure_time

@measure_time
def makeMatrix(src_doc='docs.txt'):
    """
    docs.txt からCoordinate形式の行列を作成する
    """
    
    ti_dict   = {}   # 単語と頻度の辞書
    dimention = 0    # 次元数（文脈数）

    # 単語の出現頻度を数える
    for line in open( src_doc ):
        listed_line = line.rstrip().split(',')
        for term in listed_line:
            ti_dict[term] = ti_dict.get(term, 0) + 1
        # 文脈数を数え上げる
        dimention += 1

    # n個以上出現した単語だけを保持する
    threshold = 10
    # item[0]: 単語
    # item[1]: 頻度
    uniterms = [item[0] for item in ti_dict.iteritems() \
                        if  item[1] > threshold]

    # lil_matrix形式の疎行列を生成
    lil_matrix = sparse.lil_matrix( (len(uniterms), dimention) )
    for i, term in enumerate( uniterms ):
        for j, line in enumerate( open(src_doc) ):
            val = line.rstrip().split(',').count( term )
            if val:
                lil_matrix[i,j] = float(val)

        print i # 進捗確認
    
    decoded_relation = map(lambda t: t.decode('utf_8'), uniterms) # decodeしないとloadmatができない
    io.savemat( 'matrix.mat', {'matrix':lil_matrix, 'relation':decoded_relation} )


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    # 行列生成に使うファイルを指定できる
    if argc == 2:
        makeMatrix( src_doc=argv[1] )
    else:
        makeMatrix()
