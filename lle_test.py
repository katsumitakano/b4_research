# coding: utf-8
import numpy as np
import scipy as sp
import scipy.io as spio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import sparse
from scipy.sparse import linalg as splinalg
from scipy.sparse import csgraph
from sklearn import manifold
from sklearn import datasets
from sklearn.neighbors import NearestNeighbors

def loadmat():
    """
    matrixファイルの読み込み
    """
    matfile = spio.loadmat('matrix.mat')
    return (matfile['matrix'], \
            matfile['relation'])

def find_neighbours(spmat, k):
    """
    近傍点を探索し、その位置を返す
    @p spmat: 疎行列形式の行列
    @p k: 近傍点の個数
    @r 各点に対応する近傍点の位置
    """
    neigh = NearestNeighbors()
    neigh.fit(spmat)
    indices = neigh.kneighbors(spmat, k+1, return_distance=False)
    indices = indices[:,1:] # 1列目は自分との距離なので使わない

    return indices

def solve_weights(spmat, neighs):
    """
    重み行列Wを返す
    @p spmat: 疎行列形式の行列
    @p neighs各点に対応する近傍点の位置
    @r NxNの重み行列
    """
    k = neighs.shape[1] # 近傍点の個数
    D = spmat.shape[1] # 元の行列の次元数
    N = spmat.shape[0]
    W = sparse.lil_matrix( (N,N) ) # 重み行列の宣言
    ones = np.ones(k) # 方程式の解

    for i, neigh in enumerate(neighs):
        Z  = spmat[neigh].toarray()
        Xi = spmat[i].toarray()
        Z = Z-Xi
        C = np.dot(Z, Z.T) # 分散共分散行列の計算
        # import pdb;pdb.set_trace()
        if k>D:
            # 正規化するためCに正規化定数を足す
            I = np.eye( C.shape[0] )
            eps = 0.001*C.trace()
            C += I*eps
        w = sp.linalg.solve(C, ones, sym_pos=True)
        w = w/sum(w) # 割って正規化
        W[i, neigh] = w # 近傍点の解を格納

    return W.tocsr()

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

    # sigmaがめちゃ大事らしい
    eig_value, eig_vector = splinalg.eigsh(M, d+1,\
                                           sigma=0.0,\
                                           maxiter=100)
    return eig_vector[:,1:]  # 底を除くd個の固有ベクトル


if __name__ == "__main__":
    k = 12   # 近傍点の数（8~20程度）
    d = 2   # 圧縮後の次元数

    # スイスロールのデータ読み込み
    swiss = datasets.make_swiss_roll(1000)
    data  = swiss[0]
    color = swiss[1]

    # 近傍点の取得
    spmat = sparse.csr_matrix(data)
    neighs = find_neighbours(spmat, k)
    
    # 重み行列の計算
    W = solve_weights(spmat, neighs)

    # 低次元へ埋め込み
    Y = embedding(spmat, W, d)

    plt.scatter(Y[:,0], Y[:,1], c=color)
    plt.show()

    # scikit-learnでテスト
    # lle = manifold.LocallyLinearEmbedding(n_neighbors=k,
    #                          n_components=d)
    # _Y = lle.fit_transform(data)
    # plt.scatter(_Y[:,0], _Y[:,1], c=color)
    # plt.show()
