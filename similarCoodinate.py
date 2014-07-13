# coding: utf-8
# ベクトルの類似度を計算する

import re
import sys
import math

def similar(i_l1, i_l2):
    '''
    指定された行同士のベクトル類似度を計算
    '''
    # l1 < l2にする
    if  i_l1 > i_l2: (i_l1, i_l2) = (i_l2, i_l1)

    coo_matrix = open('coordinateMatrix.dat')
    header   = coo_matrix.readline().rstrip().split(' ')
    row, col = int(header[0]), int(header[1])

    # 次元数の0ベクトルを確保
    vector1 = [0 for _ in xrange(col)]
    vector2 = [0 for _ in xrange(col)]
    for line in coo_matrix:
        i_j_val = line.rstrip().split(' ')
        i, j, val = int(i_j_val[0]), int(i_j_val[1]), float(i_j_val[2])
        if i > i_l2: break # これ以上検索する意味が無い

        if i == i_l1: vector1[j] = val
        if i == i_l2: vector2[j] = val

    return cosine(vector1, vector2)


def cosine(vector1, vector2):
    '''
    ベクトル同士のコサイン類似度を計算
    '''
    numerator = sum([vector1[i] * vector2[i] for i in xrange(len(vector1))])
    deno1 = math.sqrt( sum([v*v for v in vector1]) )
    deno2 = math.sqrt( sum([v*v for v in vector2]) )
    denominator = deno1 * deno2
    return numerator/denominator

if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)
    if argc != 3:
        print "You need 2 arguments (For example: python similer.py 単語1 単語2)"
        exit()

    t1, t2 = argv[1], argv[2]
    with open('coordinateRelation.dat') as f:
        term_dict = [v.split(' ') for v in f.readlines()]
        term_dict = dict(term_dict)

    # print "%s と %s の類似度 " % (t1, t2)
    # print similar(int(term_dict[t1]), int(term_dict[t2]))

    for k1 in term_dict.keys():
        for k2 in term_dict.keys():
            sim = similar(int(term_dict[k1]), int(term_dict[k2]))
            if sim == 0: continue
            print "%f\t%s\t%s" % (sim, k1, k2)


#------------------------テスト -----------------------------
def test():
    pass
