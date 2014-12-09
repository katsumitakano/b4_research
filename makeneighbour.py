 # coding: utf-8
import os
import sys
import numpy as np
import scipy as sp
from scipy import io as spio
from sklearn.neighbors import NearestNeighbors
from mylib import measure_time

if __name__ == "__main__":
    mat_file = spio.loadmat('matrix_co.mat')
    matrix   = mat_file['matrix']

    save_name = "neighbours.dat"
    if  os.path.isfile( save_name ):
        os.remove( save_name )
    wfile = open ( save_name, 'a' )

    N = matrix.shape[0] # データ数

    # フィッティング
    neigh = NearestNeighbors()
    neigh.fit(matrix)
    for i in xrange(N):
        # 近傍点取得(全単語との距離を格納)
        dists, indices = neigh.kneighbors(matrix[i], N,\
                                          return_distance=True)
        # 書き込み用に整形
        write_list = []
        for ind, dist in zip(indices.ravel(), dists.ravel()):
            write_list.append("%d:%.10g" % (ind, dist)) # 精度は適当…
        # 書き込み
        wfile.write( ' '.join(write_list)+'\n' )
        sys.stderr.write("makeneighbour:%d\n" % (i)) # 進捗確認
