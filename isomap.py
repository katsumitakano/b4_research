# coding: utf-8
import sys
import numpy as np
import scipy as sp
import scipy.io as spio
from scipy import sparse
from scipy.sparse import csgraph
from sklearn import manifold
from sklearn.neighbors import NearestNeighbors
from mylib import measure_time

def loadmat():
    """
    matrixファイルの読み込み
    """
    matfile = spio.loadmat('matrix_co.mat')
    return (matfile['matrix'], \
            matfile['terms'])

@measure_time
def rnn_graph(spmat, r, test=False):
    """
    疎な近傍グラフを作成する
    @p spmat: 疎行列形式の行列
    @p r: 近傍半径
    @r 疎行列形式の近傍グラフ
    """
    i = 0
    N = spmat.shape[0] # 距離行列の大きさ
    G_sparse = sparse.lil_matrix( (N,N) )

    if test:
        # --- テスト時はneighborsをそのまま使う
        neigh = NearestNeighbors()
        neigh.fit(spmat)
        dists, indices = neigh.radius_neighbors(spmat, r, return_distance=True)

        # 近傍探索グラフの作成
        for i, J in enumerate(indices):
            G_sparse[i, J[1:]] = dists[i][1:] # FancyIndex(自分との距離は使わない)
    else:
        # --- 本番時はファイルから読み込む
        fp = open("neighbours.dat", "r")
        line = fp.readline()

        # 近傍探索グラフの作成
        while line:
            neigh = line.rstrip().split()
            for idx_dist in neigh[1:]:
                idx, dist = idx_dist.split(":")
                idx  = int(idx)
                dist = float(dist)
                if dist > r:
                    break # 距離が近傍半径を超えたら終了
                else:
                    G_sparse[i, idx] = dist
            i += 1
            line = fp.readline()
            sys.stderr.write("rnn_graph:%d\n" % (i))

    return G_sparse

@measure_time
def knn_graph(spmat, k, test=False):
    """
    疎な近傍グラフを作成する
    @p spmat: 疎行列形式の行列
    @p k: 近傍点の個数
    @r 疎行列形式の近傍グラフ
    """
    i = 0
    N = spmat.shape[0] # 距離行列の大きさ
    G_sparse = sparse.lil_matrix( (N,N) )

    if test:
        # --- テスト時はneighborsをそのまま使う
        neigh = NearestNeighbors()
        neigh.fit(spmat)
        dists, indices = neigh.kneighbors(spmat, k+1, return_distance=True)
        dists   = dists[:,1:]   # 1列目は自分との距離なので使わない
        indices = indices[:,1:] # 同上

        # 近傍探索グラフの作成
        for i, J in enumerate(indices):
            G_sparse[i, J] = dists[i] # FancyIndex
    else:
        # --- 本番時はファイルから読み込む        
        fp = open("neighbours.dat", "r")
        line = fp.readline()

        # 近傍探索グラフの作成
        while line:
            neigh = line.rstrip().split()
            for idx_dist in neigh[1:k+1]:
                idx, dist = idx_dist.split(":")
                idx  = int(idx)
                dist = float(dist)
                G_sparse[i, idx] = dist
            i += 1
            line = fp.readline()
            sys.stderr.write("knn_graph:%d\n" % (i))

    return G_sparse

@measure_time
def distance_matrix(G_sparse):
    """
    グラフ形式の行列から距離行列を生成する
    @p G_sparse: 疎行列形式のグラフ
    """
    return csgraph.dijkstra(G_sparse, directed=False)

@measure_time
def MDS(D, d):
    """
    MDSにより距離行列を低次元に埋め込む
    @p D: 密な距離行列
    @p d: 埋め込み後の次元数
    """
    N = len(D)
    S = D*D # 距離の2乗
    H = np.eye(N) - np.ones((N,N))/N # 中心化行列
    P = -0.5 * H.dot(S).dot(H) # ヤング・ハウスホルダー変換(-1/2*H*S*H)
    #np.savetxt("P_isomap", P) # 行列保存
    S = None # メモリ解放
    H = None # メモリ解放

    # 固有値計算
    sys.stderr.write("Start Eigen Computation\n")
    eig_value, eig_vector = np.linalg.eigh(P)
    sys.stderr.write("End Eigen Computation\n")
    P = None # メモリ解放

    ind = np.argsort(eig_value)[::-1] # 固有値の大きい順にソート
    p = ind[:d]

    W = eig_value[p]    # 上位p個の固有値
    X = eig_vector[:,p] # 上位p個の固有ベクトル
    Y = np.sqrt(W)*X
    
    # 保存用に固有値と固有ベクトルも返却
    dmax = 1000
    if dmax > N: dmax = N
    return Y, eig_value[ind[:dmax]], eig_vector[:,ind[:dmax]]

def Isomap(spmat, k=None, r=None, d=300, test=False):
    """
    Isomapの実行
    @p spmat: 疎行列形式の行列
    @p k: 近傍点の個数
    @p d: 埋め込み後の次元数
    @p test: Trueの時swiss_rollを読み込む
    """
    suffix = ""     # 固有値、固有ベクトルの保存名に使用
    INFVAL = 100000 # 適当に大きい値(np.infと交換)

    # 近傍点の探索
    if   k != None: # k近傍の実行
        suffix = "_k%d" % (k)
        sys.stderr.write("making knn_graph\n")
        G_sparse = knn_graph(spmat, k, test)

    elif r != None: # 近傍半径の実行
        suffix = "_r%d" % (r)
        sys.stderr.write("making rnn_graph\n")
        G_sparse = rnn_graph(spmat, r, test)

    else: # 正しい引数が得られていない
        sys.stderr.write("Input k or r Value\n")
        sys.exit()

    # 測地線距離に基づく距離行列D_Gを作成
    sys.stderr.write("compute distance matrix\n")
    D_G = distance_matrix(G_sparse)
    D_G[D_G == np.inf] = INFVAL # infを適当に巨大な値に変更

    # D_GをMDSで畳み込む
    sys.stderr.write("embedding with MDS...\n")
    Y, eig_value, eig_vector = MDS(D_G, d)

    # 固有値、固有ベクトルの保存
    sys.stderr.write("saving eig_value and eig_vector...\n")
    np.save("isomap_eval"+suffix, eig_value)
    np.save("isomap_evec"+suffix, eig_vector)

    sys.stderr.write("OK!\n")
    return Y

def test(k, r, d=2):
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
    Y = Isomap(spmat, k, r, d, test=True)
    # 2次元プロット
    plt.scatter(Y[:,0], Y[:,1], c=color)
    plt.show()


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)
    usage = "Usage: isomap.py [-k|-r] 近傍点or近傍半径 圧縮後の次元 [test]\n"

    if argc != 4 and argc != 5:
        sys.stderr.write(usage)
        sys.exit()

    t = argv[1]      # 近傍のタイプ
    v = int(argv[2]) # その値
    d = int(argv[3]) # 圧縮後の次元数

    # -------------------------
    # 通常時の処理
    # -------------------------
    if argc == 4:
        spmat, terms = loadmat()
        if t == "-k":
            Y = Isomap(spmat, k=v, d=d, test=False) # k近傍
            save_name = "isomap_k%d_d%d.mat" % (v, d)
        elif t == "-r":
            Y = Isomap(spmat, r=v, d=d, test=False) # 近傍半径
            save_name = "isomap_r%f_d%d.mat" % (v, d)
        else:
            sys.stderr.write(usage)
            sys.exit()

        spio.savemat(save_name, {'Y':Y, 'terms':terms})

    # -------------------------
    # テスト時の処理
    # -------------------------
    elif argc == 5:
        if t == "-k":
            test(k=v, r=None, d=d)
        elif t == "-r":
            test(k=None, r=v, d=d)
        else:
            sys.stderr.write(usage)
            sys.exit()
        
