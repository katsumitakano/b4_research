# coding: utf-8
import sys
import numpy as np
import scipy as sp
import scipy.io as spio
from scipy import sparse
from sklearn import manifold
from sklearn import datasets
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
def find_neighbours(spmat, k, test=False):
    """
    近傍点を探索し、その位置を返す
    @p spmat: 疎行列形式の行列
    @p k: 近傍点の個数
    @r 各点に対応する近傍点の位置
    """
    i = 0
    N = spmat.shape[0] # データ数

    if test:
        # --- テスト時はneighborsをそのまま使う
        neigh = NearestNeighbors()
        neigh.fit(spmat)
        indices = neigh.kneighbors(spmat, k+1, return_distance=False)
        indices = indices[:,1:] # 1列目は自分との距離なので使わない
    else:
        # --- 本番時はファイルから読み込む        
        fp = open("neighbours.dat", "r")
        line = fp.readline()
        indices = np.empty((N, k), dtype=np.int)

        # 近傍探索グラフの作成
        while line:
            neigh = line.rstrip().split()
            for j, idx_dist in enumerate(neigh[1:k+1]):
                idx, dist = idx_dist.split(":")
                idx  = int(idx)
                indices[i, j] = idx
            i += 1
            line = fp.readline()
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
    spmat = spmat.tocsr() # 行形式の参照を速くする
    for i, neigh in enumerate(neighs):
        Z  = spmat[neigh].toarray() # 1.05ms
        Xi = spmat[i].toarray() # 152us
        Z = Z-Xi # 607us
        C = np.dot(Z, Z.T) # 分散共分散行列の計算 2.99ms
        # 正規化するためCに正規化定数を足す
        trace = C.trace() # 3.19us
        if trace > 0:
            eps = 0.001*trace
        else:
            eps = 0.001
        C += I*eps # 1.5us
        w = sp.linalg.solve(C, ones, sym_pos=True) # 45.5us
        w = w/sum(w) # 割って正規化 5.31us
        W[i, neigh] = w # 近傍点の解を格納 139us
        sys.stderr.write("solve_weights:%d\n" % (i)) # 31.7us

    return W.tocsr()

@measure_time
def embedding(W, d):
    """
    元の行列を低次元に埋め込む
    @p W: 重み行列
    @p d: 圧縮後の次元数
    @r 埋め込み後の行列
    """
    N = W.shape[0]
    I = sparse.eye(N)
    IW = I-W
    M = IW.T.dot(IW)
    M = M.toarray()
    #np.savetxt("M_lle", M) # 行列保存
    I  = None # メモリ解放
    IW = None # メモリ解放

    # 固有値計算
    sys.stderr.write("Start Eigen Computation\n")
    eig_value, eig_vector = np.linalg.eigh(M)
    sys.stderr.write("End Eigen Computation\n")
    M = None # メモリ解放

    ind = np.argsort(eig_value) # 固有値の小さい順にソート
    p = ind[1:d+1]              # 底を除くd個のインデックス

    Y = eig_vector[:,p]   # 底を除くd個の固有ベクトル

    # 保存用に固有値と固有ベクトルも返却
    dmax = 1000
    if dmax > N: dmax = N
    return Y, eig_value[ind[:dmax]], eig_vector[:,ind[:dmax]]

def LLE(spmat, k, d, test=False):
    """
    LLEの実行
    @p spmat: 疎行列形式の行列
    @p k: 近傍点の個数
    @p d: 埋め込み後の次元数
    @p test: Trueの時swiss_rollを読み込む
    """
    suffix = "_k%d" % (k)

    # 1.近傍点の取得
    sys.stderr.write("find_neighbours\n")
    neighs = find_neighbours(spmat, k, test)

    # 2.重み行列の計算
    sys.stderr.write("solve_weights\n")
    W = solve_weights(spmat, neighs)

    # 3.低次元へ埋め込み
    sys.stderr.write("embedding...\n")
    Y, eig_value, eig_vector = embedding(W, d)

    # 4.固有値、固有ベクトルの保存
    sys.stderr.write("saving eig_value and eig_vector...\n")
    np.save("lle_eval"+suffix, eig_value)
    np.save("lle_evec"+suffix, eig_vector)

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
