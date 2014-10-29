# coding: utf-8
import sys
import numpy as np
import scipy as sp
import scipy.io as spio
from scipy import sparse
from scipy.sparse import csgraph
from sklearn import manifold
from sklearn.neighbors import NearestNeighbors

def loadmat():
    """
    matrixファイルの読み込み
    """
    matfile = spio.loadmat('matrix.mat')
    return (matfile['matrix'], \
            matfile['relation'])

def knn_graph(spmat, k):
    """
    疎な近傍グラフを作成する
    @p spmat: 疎行列形式の行列
    @p k: 近傍点の個数
    @r 疎行列形式の近傍グラフ
    """
    neigh = NearestNeighbors()
    neigh.fit(spmat)
    dists, indices = neigh.kneighbors(spmat, k+1, return_distance=True)
    dists   = dists[:,1:]   # 1列目は自分との距離なので使わない
    indices = indices[:,1:] # 同上

    # 近傍探索グラフの作成
    N = len(indices) # 距離行列の大きさ
    G_sparse = sparse.lil_matrix( (N,N) )
    for i, J in enumerate(indices):
        G_sparse[i, J] = dists[i] # FancyIndex

    return G_sparse

def MDS(D, d):
    """
    MDSにより距離行列を低次元に埋め込む
    @p D: 密な距離行列
    @p d: 埋め込み後の次元数
    """
    N = len(D)
    S = D*D # 距離の2乗
    H = np.eye(N) - np.ones((N,N))/N # 中心化行列
    P = - 1.0/2 * H * S * H # ヤング・ハウスホルダー変換

    # スペクトル分解
    eig_value, eig_vector = np.linalg.eigh(P)
    ind = np.argsort(eig_value)
    p = [value for i, value \
                   in enumerate(reversed(ind)) \
                   if i < d]

    W = eig_value[p]
    X = eig_vector[:,p]  # 上位p個の固有ベクトル
    
    return np.sqrt(W)*X

def Isomap(spmat, k, d):
    """
    Isomapの実行
    @p spmat: 疎行列形式の行列
    @p k: 近傍点の個数
    @p d: 埋め込み後の次元数
    """
    INFVAL = 10000 # 適当に大きい値(np.infと交換)

    # 近傍点の探索
    G_sparse = knn_graph(spmat, k)

    # 測地線距離に基づく距離行列D_Gを作成
    D_G = csgraph.dijkstra(G_sparse, directed=False)
    D_G[D_G == np.inf] = INFVAL # infを適当に巨大な値に変更

    # D_GをMDSで畳み込む
    Y = MDS(D_G, d)

    ### mds = manifold.MDS(n_components=d, dissimilarity="precomputed")
    ### Y = mds.fit_transform(D_G)

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
    Y = Isomap(spmat, k, d)
    # 2次元プロット
    plt.scatter(Y[:,0], Y[:,1], c=color)
    plt.show()


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    if argc != 3 and argc != 4:
        print "Usage: isomap.py 近傍数 圧縮後の次元 [test]"
        sys.exit()

    k = int(argv[1]) # 近傍点の数
    d = int(argv[2]) # 圧縮後の次元数

    if argc == 3:   # 通常時
        spmat, terms = loadmat()
        Y = Isomap(spmat, k, d)
        print Y
    elif argc == 4: # テスト実行
        test(k, d)

        
