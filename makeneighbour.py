# coding: utf-8
import os
import sys
import numpy as np
import scipy as sp
from scipy import io as spio

if __name__ == "__main__":
    mat_file = spio.loadmat('matrix.mat')
    matrix   = mat_file['matrix']
    relation = mat_file['relation']

    save_name = "neighbours.dat"
    if  os.path.isfile( save_name ):
        os.remove( save_name )
    wfile = open ( save_name, 'a' )

    N = matrix.shape[0]
    dists = np.empty(N, dtype=np.float64)
    for i in xrange(N):
        A = matrix[i]
        for j in xrange(N):
            # 距離計算
            B = matrix[j]
            d = np.linalg.norm( (A-B).toarray() )
            dists[j] = d
        # 書き込み
        ind = dists.argsort()[:100]
        write_list = []
        for index, dist in zip(ind, dists[ind]):
            write_list.append("%d:%.4f" % (index, dist))
        wfile.write( ' '.join(write_list)+'\n' )
        sys.stderr.write("makeneighbour:%d\n" % (i)) # 進捗確認
