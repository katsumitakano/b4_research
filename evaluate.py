# coding: utf-8
import sys
import codecs
import cPickle as pickle
import numpy as np
from numpy.linalg import norm
from pandas import DataFrame
from scipy import io as spio
from mylib import measure_time


def sim_cosine(vector1, vector2):
    """ 2つのベクトルを受け取り、コサイン類似度を返す """
    return np.dot(vector1, vector2)/(norm(vector1)*norm(vector2))


def F_ave( matrix, relation, n_max ):
    """
    n_maxまでの平均F値の計算
    """
    M = matrix['Y']
    terms = matrix['terms']
    terms = map(lambda t: t.rstrip(), terms) # 末尾の空白削除

    result = [] # F_nの値を保持
    sigeki_bunrui = relation.dropna()

    for sigeki in sigeki_bunrui.index:
        bunrui = sigeki_bunrui[sigeki]
        # sigeki: 刺激語
        # bunrui: ある関係における刺激語に対する分類語

        # 単語の存在をチェック
        bunrui = set(bunrui) & set(terms) # 存在しない分類語を省く
        if len(bunrui) == 0: continue
        try:
            index = terms.index(sigeki)
        except:
            sys.stderr.write("%s not in\n" % (sigeki.encode("utf-8")))
            continue                      # 存在しない刺激語を省く

        # 刺激語を元に行列をソート
        sigeki_vec = M[index]
        sims = np.array([sim_cosine(sigeki_vec, vec) for vec in M])
        sorted_indices = sims.argsort()[::-1]

        tmp = [] # n_maxまでの計算結果を一時格納
        for n in xrange(100, n_max+100, 100):
            n_indices = sorted_indices[:n]
            n_terms = set( [terms[idx] for idx in n_indices] )
            R = len( bunrui & n_terms )
            C = len( bunrui )
            N = float(n)
            Recall    = float(R)/C # 再現率
            Precision = float(R)/N # 適合率
            F = 2.0*R/(C+N)        # F値（式変形）
            tmp.append(Recall)

        result.append( np.array(tmp).mean() )
#        print len(bunrui), tmp

    return np.array(result).mean()

@measure_time
def evaluate( mat_name ):
    """
    全関係の評価値を計算する
    """
    # 評価用データの読み込み
    with open('eval_data.pkl', 'r') as f:
        relation = pickle.load(f)

    # 行列ファイルを読み込み、
    matrix = spio.loadmat( mat_name )
    #df_matrix = DataFrame( matrix['Y'], index=matrix['terms'] )

    # 上位10%までみる
    n_max = 100 * ( len(matrix['terms']) / 1000 )

    # 全関係で平均F値を取る
    for column in relation.columns:
        print column
        print F_ave( matrix, relation[column], n_max )


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    if argc != 2:
        sys.stderr.write("Usage: python evaluate.py 行列ファイル名\n")
        sys.exit
    else:
        evaluate( mat_name=argv[1] )
