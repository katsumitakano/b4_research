# coding: utf-8
import sys
import numpy as np
import scipy as sp
import scipy.io as spio
import scipy.sparse.linalg as splinalg
from scipy import sparse
from mylib import measure_time

def loadmat():
    """
    matrixファイルの読み込み
    """
    matfile = spio.loadmat('matrix.mat')
    return (matfile['matrix'], \
            matfile['terms'])


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    if argc != 2:
        sys.stderr.write("Usage: svd.py 圧縮後の次元\n")
        sys.exit()

    d = int(argv[1]) # 圧縮後の次元数
    print d

    spmat, terms = loadmat()
    
    # SVDの実行
    sys.stderr.write("Start SVD\n")
    U, S, V = splinalg.svds(spmat, k=d)
    sys.stderr.write("End SVD\n")

    Y = U*S # 次元圧縮

    # 行列ファイルの保存
    save_name = "svd_d%d.mat" % (d)
    spio.savemat(save_name, {'Y':Y, 'terms':terms})
