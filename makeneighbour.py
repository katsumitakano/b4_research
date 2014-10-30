 # coding: utf-8
import os
import sys
import numpy as np
import scipy as sp
from scipy import io as spio
from sklearn.neighbors import NearestNeighbors
from mylib import measure_time

if __name__ == "__main__":
    mat_file = spio.loadmat('matrix.mat')
    matrix   = mat_file['matrix']
    # relation = mat_file['relation']

    save_name = "neighbours.dat"
    if  os.path.isfile( save_name ):
        os.remove( save_name )
    wfile = open ( save_name, 'a' )

    k = 100 # 近傍点の個数
    N = matrix.shape[0] # データ数

    # フィッティング
    neigh = NearestNeighbors()
    neigh.fit(matrix)
    for i in xrange(N):
        # 近傍点取得
        dists, indices = neigh.kneighbors(matrix[i], k,\
                                          return_distance=True)
        # 書き込み用に整形
        write_list = []
        for ind, dist in zip(indices.ravel(), dists.ravel()):
            write_list.append("%d:%.20g" % (ind, dist)) # 精度は適当…
        # 書き込み
        wfile.write( ' '.join(write_list)+'\n' )
        sys.stderr.write("makeneighbour:%d\n" % (i)) # 進捗確認
