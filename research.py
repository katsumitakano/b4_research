# coding: utf-8
import sys
import numpy as np
import scipy as sp
from scipy import io
from numpy.linalg import norm

# ---------- ファイルの読み込み ---------- #
filename = raw_input("Input matrix name (***.mat) -> ")

try:
    mat_file = io.loadmat(filename)
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

def print_top(term, n):
    """与えられた単語と類似度が高い上位n件を表示"""
    index = terms.index(term)
    tgt_vec = matrix[index]
    # 全単語との類似度を計算
    sims = np.array([sim_cosine(tgt_vec, vec) for vec in matrix])
    # 類似度の高い順にソート
    ranking = sims.argsort()[::-1]
    # 上位n件の位置と類似度を取得（1つ目は同じ単語なので無視）
    top_indices = ranking[1:n+1]
    top_sims = sims[top_indices]
    # 結果を表示
    for i in xrange(n):
        print terms[top_indices[i]], top_sims[i]


# ---------- 自作インタプリターの起動 ---------- #
while(1):
    input_line = raw_input("terms? -> ").decode('utf-8')
    input_list = input_line.split()

    if input_line == "":
        # 入力が無い場合はそのまま続ける
        continue

    elif input_list[0] == "quit":
        # quitが入力されたら終了
        print "Good Bye"
        sys.exit()

    elif len(input_list) == 1:
        # 単語1つ： 類似度が高い上位n件を表示
        try:
            ind = terms.index(input_list[0])
        except ValueError:
            print("No such term: %s" % (input_list[0]))
            continue
        print_top(input_list[0], 10)

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
        print("調べたい単語を1つ、または2つ入力して下さい。")
