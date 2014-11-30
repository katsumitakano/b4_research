# coding: utf-8
import re
import codecs
import pandas as pd
from numpy import nan
from pandas import Series, DataFrame

# 熟語 随伴 統語 全体-部分 カテゴリ-事例 類義語 反意語 事例-事例
filelist = ['idiom_Rate.dat', 'co_exist_Rate.dat', 'syntactic_Rate.dat', \
'part_of_Rate.dat', 'member_of_Rate.dat', 'synonym_Rate.dat', 'antnym_Rate.dat', \
'same_member_Rate.dat']

# 「あたま/頭」のようなデータのうち、どちらを選択するかまとめた配列
priority = [u"ジャズ", u"鑑賞", u"行く", u"虎", u"衝突", u"スクール", u"イマジネーション", u"ミュージック", u"パーク", u"目", u"便り", u"薬", u"船", u"良い", u"ピクニック", u"ニュース", u"大変", u"頭", u"コマーシャル", u"花", u"うさぎ", u"無し", u"バス", u"イメージ", u"町", u"柵", u"道", u"木", u"卑怯", u"馬鹿", u"嫌い", u"魂", u"ラブ", u"無い", u"機械"] # 合計35個

# 評価に使う刺激語を選択
eval_sigeki = []
with codecs.open('eval_data/idiom_Rate.dat', 'r', 'utf-8') as f:
    for line in f.readlines()[2:]: # 最初の2行は飛ばす
        eval_sigeki.append( line.split('-')[0] )

eval_sigeki = list(set(eval_sigeki))


# pandasで表形式のデータを作成する
# index × columnsの空配列作成
col = len(filelist)
row = len(eval_sigeki)
data = [ [ [] for _ in xrange(col) ] for _ in xrange(row) ] # 空リストを要素に持つDataFrameを生成
tables = DataFrame(data, columns=filelist, index=eval_sigeki)

# 分類データを読み込んで表を生成
for filename in filelist:
    f = codecs.open( "eval_data/"+filename, "r", "utf-8" )
    eval_data = f.readlines()[2:] # 最初の2行は捨てる
    eval_data = [ l.rstrip() for l in eval_data ] # 改行文字削除
    # 行を分割して対応した表の位置にぶち込んでく
    for line in eval_data:
        data = re.split(r'-|: |\(', line)
        sigeki = data[0]        # 刺激語
        renso  = data[1]        # 連想語
        if "/" in renso:        # 連想語のチェック
            for pick in renso.split("/"):
                if pick in priority: # 「単語1/単語2」のうち、優先度の高い方を選択
                    renso = pick
                    break
        rate   = float(data[2]) # 比率（ 例：0.80 ）
        ans    = data[3][:-1]   # 回答数（ 例：4/5 ）
        # 過半数を超えた連想語のみ採用
        if rate >= 0.6:
            tables[filename][sigeki].append(renso)

# 空配列をNaNに変換
for c in tables.columns:
    for i in tables.index:
        if tables[c][i] == []:
            tables[c][i] = nan

# 分類の対の数を表示
for column in filelist:
    renso_num = 0
    for renso_list in tables[column].dropna():
        renso_num += len(renso_list)
    print(column, renso_num)


# 評価用使う全ての単語を取得
eval_all = []
for column in filelist:
    for renso_list in tables[column].dropna():
        eval_all.extend(renso_list)
eval_all = list(set(eval_all))


# ---------------------------------------
# --- 各種データの書き出し
# ---------------------------------------

eval_sigeki = [t+"\n" for t in eval_sigeki]
with codecs.open("eval_sigeki.txt", "w", "utf-8") as f:
    f.writelines(eval_sigeki)

eval_all = [t+"\n" for t in eval_all]
with codecs.open("eval_all.txt", "w", "utf-8") as f:
    f.writelines(eval_all)

tables.to_pickle("eval_data.pkl")
