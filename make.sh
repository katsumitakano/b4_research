#!/bin/sh

# ディレクトリ名に使用
DIR_DATE=`date +"%m%d_%H%M%S"`

# 行列の作成と類似度の計算
python makedocs.py $1 docs.txt
python makematrix.py
python cosine.py

# 作成したデータをarchiveに移す
mkdir archive/${DIR_DATE}
cp docs.txt archive/${DIR_DATE}
cp matrix.mat archive/${DIR_DATE}
cp cosine.txt archive/${DIR_DATE}


# 以下のプログラムが追加されていく？
# python lsi.py
# python isomap.py
# python lle.py
# python deeplearning.py

