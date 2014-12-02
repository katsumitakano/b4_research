# coding: utf-8
import codecs

terms = []                      # 行列に含まれる全単語
eval_sigeki = []                # 評価に使う刺激後
eval_all = []                   # 評価に使う単語全て
counter = 0                     # 単語が含まれなかった数を格納

# データの読み込み
with codecs.open("terms.txt", "r", "utf-8") as f:
    terms = [line.rstrip() for line in f.readlines()]
with codecs.open("eval_all.txt", "r", "utf-8") as f:
    eval_all = [line.rstrip() for line in f.readlines()]
with codecs.open("eval_sigeki.txt", "r", "utf-8") as f:
    eval_sigeki = [line.rstrip() for line in f.readlines()]

# 集合型に変換
terms = set(terms)
eval_all = set(eval_all)
eval_sigeki = set(eval_sigeki)

# 含まれていない単語を抽出
notin_sigeki = (eval_sigeki - terms)
notin_all    = (eval_all - terms)

# 結果の表示
print "--- Sigeki Terms ---"
for term in notin_sigeki:
    print term
print "%d terms not in\n" % len(notin_sigeki)

print "--- All Terms ---"
for term in notin_all:
    print term
print "%d terms not in\n" % len(notin_all)
