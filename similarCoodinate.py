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

    # 【一時的！！】文脈数を889と決め打ち
    vector1 = [0 for _ in range(889)]
    vector2 = [0 for _ in range(889)]
    for line in open('coordinateMatrix.dat'):
        i_j_val = line.split(' ')
        i, j, val = int(i_j_val[0]), int(i_j_val[1]), float(i_j_val[2].rstrip())
        if i > i_l2: break # これ以上検索する意味が無い

        if i == i_l1: vector1[j] = val
        if i == i_l2: vector2[j] = val

#    print vector1
#    print vector2
    return cosine(vector1, vector2)


def cosine(vector1_i, vector2_i):
    '''
    ベクトル同士のコサイン類似度を計算
    '''
    numerator = sum([vector1_i[i] * vector2_i[i] for i in xrange(len(vector1_i))])
    deno1 = math.sqrt( sum([v*v for v in vector1_i]) )
    deno2 = math.sqrt( sum([v*v for v in vector2_i]) )
    denominator = float(deno1 * deno2)
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

    print "%s と %s の類似度 " % (t1, t2)
    print similar(int(term_dict[t1]), int(term_dict[t2]))

    # for k1 in term_dict.keys():
    #     for k2 in term_dict.keys():
    #         sim = similar(int(term_dict[k1]), int(term_dict[k2]))
    #         if sim == 0: continue
    #         print "%s\t%s\t%f" % (k1, k2, sim)


#------------------------テスト -----------------------------
def test():
    pass
