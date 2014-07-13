# coding: utf-8
# ベクトルの類似度を計算する

import sys
import math

def similar(l1, l2):
    '''
    指定された行同士のベクトル類似度を計算
    '''
    l1, l2 = int(l1), int(l2)
    # l1 < l2にする
    if l1 > l2:
        (l1, l2) = (l2, l1)

    with open('matrix.dat') as f:
        for _ in xrange(l1-1): f.readline()
        vector1 = f.readline().split(' ')
        for _ in xrange((l2-l1)-1): f.readline()
        vector2 = f.readline().split(' ')

    vector1 = [int(v) for v in vector1]
    vector2 = [int(v) for v in vector2]

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
        print "You need 2 arguments (For example: python similer.py 13 42)"
        exit()

    t1, t2 = argv[1], argv[2]
    with open('relation.dat') as f:
        term_dict = [v.split(' ') for v in f.readlines()]
        term_dict = dict(term_dict)

#    print "%s と %s の類似度" % (t1, t2)
#    print similar(term_dict[t1], term_dict[t2])

    for k1 in term_dict.keys():
        for k2 in term_dict.keys():
            sim = similar(term_dict[k1], term_dict[k2])
            if sim == 0: continue
            print "%f\t%s\t%s" % (sim, k1, k2)


#------------------------テスト -----------------------------
def test():
    pass
