 # coding: utf-8
import os
import sys
import numpy as np
import scipy as sp
from scipy import io as spio
from sklearn import metrics
from sklearn.neighbors import NearestNeighbors
from mylib import measure_time

mat_file = spio.loadmat('matrix_co.mat')
matrix   = mat_file['matrix']

save_name = "neighbours.dat"
if  os.path.isfile( save_name ):
    os.remove( save_name )
wfile = open ( save_name, 'a' )

@measure_time
def euclid_neighbor():
    """近傍点をユークリッド距離で計算"""
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
        sys.stderr.write("makeneighbour(euc):%d\n" % (i)) # 進捗確認

@measure_time
def cosine_neighbor():
    """近傍点をコサイン距離で計算"""
    cosine_sim_matrix = metrics.pairwise.cosine_distances(matrix)

    for i, col in enumerate(cosine_sim_matrix):
        neighs = np.argsort(col)
        # 書き込み用に整形
        write_list = []
        for ind, dist in zip(neighs, col[neighs]):
            write_list.append("%d:%.10g" % (ind, dist)) # 精度は適当…
        # 書き込み
        wfile.write( ' '.join(write_list)+'\n' )
        sys.stderr.write("makeneighbour(cos):%d\n" % (i)) # 進捗確認

if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    if argc != 2 or argv[1] not in ["euclid", "cosine"]:
        sys.stderr.write("Usage: python makeneighbour.py [euclid|cosine]")

    neigh_type = argv[1]
    if   neigh_type == "euclid":
        euclid_neighbor()
    elif neigh_type == "cosine":
        cosine_neighbor()
