# coding: utf-8
import sys
import numpy as np
import scipy as sp
import scipy.io as spio
from scipy import sparse
from scipy.sparse import linalg as splinalg
from scipy.sparse import csgraph
from sklearn import manifold
from sklearn import datasets
from sklearn.neighbors import NearestNeighbors
from mylib import measure_time

def loadmat():
    """
    matrixファイルの読み込み
    """
    matfile = spio.loadmat('matrix.mat')
    return (matfile['matrix'], \
            matfile['terms'])

@measure_time
def find_neighbours(spmat, k, test=False):
    """
    近傍点を探索し、その位置を返す
    @p spmat: 疎行列形式の行列
    @p k: 近傍点の個数
    @r 各点に対応する近傍点の位置
    """
    N = spmat.shape[0] # データ数

    if test:
        # --- テスト時はneighborsをそのまま使う
        neigh = NearestNeighbors()
        neigh.fit(spmat)
        indices = neigh.kneighbors(spmat, k+1, return_distance=False)
        indices = indices[:,1:] # 1列目は自分との距離なので使わない
    else:
        # --- 本番時はファイルから読み込む        
        neighs = np.loadtxt('neighbours.dat', delimiter=" ", dtype="S")
        neighs = neighs[:,1:k+1]
        indices = np.empty(neighs.shape, dtype=np.int)

        # 近傍探索グラフの作成
        for i, neigh in enumerate(neighs):
            for j, idx_dist in enumerate(neigh):
                idx, dist = idx_dist.split(":")
                idx  = int(idx)
                indices[i, j] = idx
            sys.stderr.write("knn_graph:%d\n" % (i))

    return indices

@measure_time
def solve_weights(spmat, neighs):
    """
    重み行列Wを返す
    @p spmat: 疎行列形式の行列
    @p neighs: 各点に対応する近傍点の位置
    @r NxNの重み行列
    """
    k = neighs.shape[1] # 近傍点の個数
    D = spmat.shape[1]  # 元の行列の次元数
    N = spmat.shape[0]  # データ数
    I = np.eye(k)       # 単位行列
    ones = np.ones(k)   # 方程式の解

    W = sparse.lil_matrix( (N,N) ) # 重み行列の宣言
    for i, neigh in enumerate(neighs):
        Z  = spmat[neigh].toarray()
        Xi = spmat[i].toarray()
        Z = Z-Xi
        C = np.dot(Z, Z.T) # 分散共分散行列の計算
        # 正規化するためCに正規化定数を足す
        trace = C.trace()
        if trace > 0:
            eps = 0.001*trace
        else:
            eps = 0.001
        C += I*eps
        w = sp.linalg.solve(C, ones, sym_pos=True)
        w = w/sum(w) # 割って正規化
        W[i, neigh] = w # 近傍点の解を格納
        sys.stderr.write("solve_weights:%d\n" % (i))

    return W.tocsr()

@measure_time
def embedding(spmat, W, d):
    """
    元の行列を低次元に埋め込む
    @p spmat: 疎行列形式の行列
    @p W: 重み行列
    @p d: 圧縮後の次元数
    @r 埋め込み後の行列
    """
    N = W.shape[0]
    I = sparse.eye(N)
    M = sp.dot( (I-W).T, (I-W) )

    # 固有値計算（sigmaがめちゃ大事らしい）
    sys.stderr.write("Start Eigen Computation\n")
    eig_value, eig_vector = splinalg.eigsh(M, d+1,\
                                           sigma=0.0,\
                                           maxiter=100)
    sys.stderr.write("End Eigen Computation\n")

    return eig_vector[:,1:]  # 底を除くd個の固有ベクトル

def LLE(spmat, k, d, test=False):
    """
    LLEの実行
    @p spmat: 疎行列形式の行列
    @p k: 近傍点の個数
    @p d: 埋め込み後の次元数
    @p test: Trueの時swiss_rollを読み込む
    """
    # 1.近傍点の取得
    sys.stderr.write("find_neighbours\n")
    neighs = find_neighbours(spmat, k, test)
    # 2.重み行列の計算
    sys.stderr.write("solve_weights\n")
    W = solve_weights(spmat, neighs)
    # 3.低次元へ埋め込み
    sys.stderr.write("embedding...\n")
    Y = embedding(spmat, W, d)
    sys.stderr.write("OK!\n")
    return Y

def test(k, d):
    """
    テスト実行
    """
    from sklearn import datasets
    import matplotlib.pyplot as plt
    # スイスロールのデータ読み込み
    swiss = datasets.make_swiss_roll(1000)
    data  = swiss[0]
    color = swiss[1]
    spmat = sparse.csr_matrix(data)
    # Isomap実行
    Y = LLE(spmat, k, d, test=True)
    # 2次元プロット
    plt.scatter(Y[:,0], Y[:,1], c=color)
    plt.show()

if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    if argc != 3 and argc != 4:
        sys.stderr.write("Usage: lle.py 近傍数 圧縮後の次元 [test]\n")
        sys.exit()

    k = int(argv[1])   # 近傍点の数（8~20程度）
    d = int(argv[2])   # 圧縮後の次元数

    if argc == 3:   # 通常時
        spmat, terms = loadmat()
        Y = LLE(spmat, k, d, test=False)
        save_name = "lle_k%d_d%d.mat" % (k, d)
        spio.savemat(save_name, {'Y':Y, 'terms':terms})
    elif argc == 4: # テスト実行
        test(k, d)
