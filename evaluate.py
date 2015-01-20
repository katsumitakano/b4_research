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


def Retrieval_eval( matrix, relation, n_max, eval_type ):
    """
    n_maxまでの平均F値、または平均再現率の計算
    """
    M = matrix['Y']
    terms = matrix['terms']
    terms = map(lambda t: t.rstrip(), terms) # 末尾の空白削除

    result = [] # F_nの値を保持
    sigeki_bunrui = relation.dropna()
    count_total = 0
    count_exist = 0

    for sigeki in sigeki_bunrui.index:
        bunrui = sigeki_bunrui[sigeki]
        count_total += len(bunrui)
        # sigeki: 刺激語
        # bunrui: ある関係における刺激語に対する分類語

        # 単語の存在をチェック
        bunrui = set(bunrui) & set(terms) # 存在しない分類語を省く
        if len(bunrui) == 0: continue
        try:
            index = terms.index(sigeki)
        except:
            #sys.stderr.write("%s not in\n" % (sigeki.encode("utf-8")))
            continue                      # 存在しない刺激語を省く
        count_exist += len(bunrui)

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
            if   eval_type == "F": tmp.append(F)
            elif eval_type == "R": tmp.append(Recall)

        result.append( np.array(tmp).mean() )

    print "%d/%d" % ( count_exist, count_total ) # 評価した単語対の表示
    return np.array(result).mean()

def Rank_eval( matrix, relation, eval_type ):
    """
    分類語のランクの平均値、または中央値を計算
    """
    M = matrix['Y']
    terms = matrix['terms']
    terms = map(lambda t: t.rstrip(), terms) # 末尾の空白削除

    result = []
    sigeki_bunrui = relation.dropna()
    count_total = 0
    count_exist = 0

    for sigeki in sigeki_bunrui.index:
        bunrui = sigeki_bunrui[sigeki]
        count_total += len(bunrui)
        # sigeki: 刺激語
        # bunrui: ある関係における刺激語に対する分類語

        # 単語の存在をチェック
        bunrui = set(bunrui) & set(terms) # 存在しない分類語を省く
        if len(bunrui) == 0: continue
        try:
            index = terms.index(sigeki)
        except:
            #sys.stderr.write("%s not in\n" % (sigeki.encode("utf-8")))
            continue                      # 存在しない刺激語を省く
        count_exist += len(bunrui)

        # 刺激語を元に行列をソート
        sigeki_vec = M[index]
        sims = np.array([sim_cosine(sigeki_vec, vec) for vec in M])
        sorted_indices = sims.argsort()[::-1]

        for bun in bunrui:
            sorted_terms = [terms[idx] for idx in sorted_indices]
            rank = sorted_terms.index(bun) + 1
            result.append( rank )
            #print bun, rank

    print "%d/%d" % ( count_exist, count_total ) # 評価した単語対の表示

    if eval_type == "mean":
        return np.array(result).mean()
    elif eval_type == "median":
        return int(np.median(np.array(result)))

@measure_time
def evaluate( mat_name, eval_type ):
    """
    全関係の評価値を計算する
    """
    # 評価用データの読み込み
    with open('eval_data.pkl', 'r') as f:
        relation = pickle.load(f)

    # 行列ファイルを読み込み、
    matrix = spio.loadmat( mat_name )

    # 上位10%までみる
    n_max = 100 * ( len(matrix['terms']) / 1000 )

    # 全関係で評価値を取る
    for column in relation.columns:
        print column
        if eval_type in ["F", "R"]:
            # F値または再現率の評価
            print Retrieval_eval( matrix, relation[column], n_max, eval_type )
        elif eval_type in ["mean", "median"]:
            # ランクの平均値または中央値の評価
            print Rank_eval( matrix, relation[column], eval_type )


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    if argc != 3:
        sys.stderr.write("Usage: python evaluate.py 行列ファイル名 -評価指標\n")
        sys.exit()
    else:
        mat_name = argv[1]
        eval_type = argv[2][1:]

        # 評価のタイプをチェック
        if eval_type not in ["F", "R", "mean", "median"]:
            sys.stderr.write("eval_type: F or R or mean or median\n")
            sys.exit()

        evaluate( mat_name=argv[1], eval_type=eval_type )
