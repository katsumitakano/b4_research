# coding: utf-8
import numpy as np
import scipy as sp
import scipy.io as spio
from scipy import sparse
from scipy.sparse import csgraph
from sklearn import manifold
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

def MDS(D, n_components):
    N = len(D)
    S = D*D # 距離の2乗
    H = np.eye(N) - np.ones((N,N))/N # 中心化行列
    P = - 1.0/2 * H * S * H # ヤング・ハウスホルダー変換

    # スペクトル分解
    eig_value, eig_vector = np.linalg.eig(P)
    ind = np.argsort(eig_value)
    p = [value for i, value \
                   in enumerate(reversed(ind)) \
                   if i < n_components]

    W = P.std(axis=0)[p] # 上位p個の固有値の標準偏差
    X = eig_vector[:,p]  # 上位p個の固有ベクトル
    
    return W*X

if __name__ == "__main__":
    k = 4   # 近傍点の数
    n = 100 # 圧縮後の次元数

    # 疎行列データの読み込み
    spmat, terms = loadmat()

    # 近傍点の探索
    G_sparse = knn_graph(spmat, k)

    # 測地線距離に基づく距離行列D_Gを作成
    D_G = csgraph.dijkstra(G_sparse, directed=False)

    # D_GをMDSで畳み込む
    Y = MDS(D_G, n)

