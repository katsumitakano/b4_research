# coding: utf-8
# ベクトルの類似度を計算する

import os
import sys
import codecs
import numpy as np
from math  import sqrt
from scipy import io, sparse
from mylib import measure_time

@measure_time
def calcCosineSim( mat_name='matrix_co.mat', put_name='cosine.dat' ):
    '''
    行列からCosine類似度を計算し、単語間の類似度をFileに出力する

    @mat_name: 入力となる行列のファイル名
    @put_name: 出力するファイルの名前
    '''
    loaded_mat = io.loadmat( mat_name )
    csc_mat  = loaded_mat['matrix']
    relation = loaded_mat['terms']

    # 書き込みファイルの準備
    if  os.path.isfile( put_name ):
        os.remove( put_name )
    wfile = codecs.open( put_name, 'a', 'utf-8')

    # 計算してファイルに出力
    doted = csc_mat.dot( csc_mat.T )
    print "end doted"
    multi = csc_mat.multiply( csc_mat ).sum( axis=True )
    print "end multi"
    nonzero = doted.nonzero()
    print "end nonzero"
    end = len( nonzero[0] )

    for n in xrange(end):
        i, j = nonzero[0][n], nonzero[1][n]
        if i >= j: continue
        numera = doted[i,j]
        denomi = sqrt(multi[i]*multi[j])
        sim = numera/denomi
        wfile.write( "%f\t%s\t%s\n" % \
                         (sim, relation[i], relation[j]) )
        print "cosine:%d/%d" % (n, end) # 進捗確認


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    # 入力のファイル名と出力のファイル名を受け取る
    if argc == 3:
        calcCosineSim( mat_name=argv[1], put_name=argv[2] )
    else:
        calcCosineSim()
