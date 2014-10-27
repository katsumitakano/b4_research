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
    matfile = spio.loadmat('matrix.mat')
    return (matfile['matrix'], \
            matfile['relation'])

def knn_graph(spmat, k=4):
    neigh = NearestNeighbors()
    neigh.fit(spmat)
    dists, indices = neigh.kneighbors(spmat, k+1, return_distance=True)
    dists   = dists[:,1:]   # 1列目は自分との距離なので使わない
    indices = indices[:,1:] # 同上

    # 近傍探索グラフの作成
    N = len(indices) # 距離行列の大きさ
    G_sparse = sparse.lil_matrix( (N,N) )
    for i, J in enumerate(indices):
        for j, index in enumerate(J):
            # TODO: 分かりづらいし遅い
            G_sparse[i,index] = dists[i,j]

    return G_sparse


if __name__ == "__main__":
    k = 20   # 近傍点の数
    n = 2   # 圧縮後の次元数

    # スイスロールのデータ読み込み
    swiss = datasets.make_swiss_roll(500)
    data  = swiss[0]
    color = swiss[1]

    # 近傍グラフの作成
    spmat = sparse.csr_matrix(data)
    Z = knn_graph(spmat, k)

    # 共分散行列の計算
    C = Z.T*Z

    # 重み行列Wの計算
    N = C.shape[0]
    w = splinalg.spsolve(C, np.ones(N))
    wsum = np.sum(w)
    W = sparse.lil_matrix( (N,N) )
    for i, J in enumerate(Z.rows):
        for j in J:
            W[i,j] = w[i]/wsum # 遅いはず
    
    W = W.tocsr()
    I = sparse.csr_matrix( np.eye(N) )
    IW = (I-W)
    M = IW.T * IW

    # スペクトル分解
    eig_value, eig_vector = np.linalg.eig(M.toarray())
    ind = np.argsort(eig_value)
    p = ind[1:n+1]

    Va = eig_value[p]
    Ve = eig_vector[:,p]  # 上位p個の固有ベクトル
    
    Y = Va*Ve
    plt.scatter(Y[:,0], Y[:,1], c=color)
    plt.show()

    # scikit-learnでテスト
    # lle = manifold.LocallyLinearEmbedding(n_neighbors=k,
    #                          n_components=2)
    # _Y = lle.fit_transform(data)
    # plt.scatter(_Y[:,0], _Y[:,1], c=color)
    # plt.show()
