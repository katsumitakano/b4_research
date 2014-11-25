# coding: utf-8
import codecs

terms = []                      # 行列に含まれる全単語
eval_terms = []                 # 評価に使う刺激後
counter = 0                     # 刺激語が含まれなかった数を格納

# データの読み込み
with codecs.open("terms.txt", "r", "utf-8") as f:
    terms = [line.rstrip() for line in f.readlines()]
with codecs.open("eval_all.txt", "r", "utf-8") as f:
    eval_terms = [line.rstrip() for line in f.readlines()]

# 評価データが含まれてるかチェック
for eval in eval_terms:
    if eval not in terms:
        counter += 1
        print(eval)

# 結果の表示
if counter == 0:
    print("all in!!")
else:
    print("%d/%d terms not in." % (counter, len(eval_terms)))
