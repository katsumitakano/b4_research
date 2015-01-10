# coding: utf-8
import re
import sys
import numpy as np
import scipy as sp
from scipy import io
from numpy.linalg import norm

# ---------- ファイルの読み込み ---------- #
filename = sys.argv[1]

try:
    mat_file = io.loadmat(filename)
    print("Matfile loaded!")
except:
    sys.stderr.write("Not correct matrix name!\n")
    sys.exit()

matrix = mat_file['Y']          # np.array型
terms  = mat_file['terms']      # list型
terms = map(lambda t: t.rstrip(), terms) # 末尾の空白削除


# ---------- 関数の定義 ---------- #
def sim_cosine(vector1, vector2):
    """コサイン類似度を返す"""
    return np.dot(vector1, vector2)/(norm(vector1)*norm(vector2))

def sim_euclid(vector1, vector2):
    """ユークリッド距離を返す（値が小さいほうが近い）"""
    return -norm(vector1 - vector2)

def print_top(term, n, sim_func=sim_cosine):
    """与えられた単語と類似度が高い上位n件を表示"""
    index = terms.index(term)
    tgt_vec = matrix[index]
    # 全単語との類似度を計算
    sims = np.array([sim_func(tgt_vec, vec) for vec in matrix])
    # 類似度の高い順にソート
    ranking = sims.argsort()[::-1]
    # 上位n件の位置と類似度を取得（1つ目は同じ単語なので無視）
    top_indices = ranking[1:n+1]
    top_sims = sims[top_indices]
    # 結果を表示
    for i in xrange(n):
        print terms[top_indices[i]], top_sims[i]


# ---------- 自作インタプリターの起動 ---------- #
sim_func = sim_cosine
top_n = 10 # 上位何件表示するか
while(1):
    input_line = raw_input("terms? -> ").decode('utf-8')
    input_list = input_line.split()

    if input_line == "":
        # 入力が無い場合はそのまま続ける
        continue

    elif input_list[0] in ["quit", "exit"]:
        # quit か exit が入力されたら終了
        print "Good Bye"
        sys.exit()

    elif input_list[0] in [ ":c", ":cosine" ]:
        # 類似度計算をコサイン類似度に変更
        print("Change simType to \"cosine\"")
        sim_func = sim_cosine; continue

    elif input_list[0] in [ ":e", ":euclid" ]:
        # 類似度計算をユークリッド距離に変更
        print("Change simType to \"euclid\"")
        sim_func = sim_euclid; continue

    elif re.match(r':\d+', input_list[0]):
        # :[数字]にマッチしたら表示件数を変更
        top_n = int(input_list[0][1:])
        print("Change top_n to %d" % (top_n))

    elif len(input_list) == 1:
        # 単語1つ： 類似度が高い上位n件を表示
        try:
            ind = terms.index(input_list[0])
        except ValueError:
            print("No such term: %s" % (input_list[0]))
            continue
        target = input_list[0]
        print_top(target, top_n, sim_func)

    elif len(input_list) == 2:
        # 単語2つ： 2単語間のコサイン類似度を計算
        try: ind1 = terms.index(input_list[0])
        except ValueError:
            print("No such term: %s" % (input_list[0]))
            continue

        try: ind2 = terms.index(input_list[1])
        except ValueError:
            print("No such term: %s" % (input_list[1]))
            continue
        print sim_cosine(matrix[ind1], matrix[ind2])

    else:
        # 引数エラー
        print("調べたい単語を1つ、または2つ入力して下さい。")
