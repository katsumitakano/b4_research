#!/bin/sh

# ディレクトリ名に使用
DIR_DATE=`date +"%m%d_%H%M%S"`

# 行列の作成と類似度の計算
python makedocs.py $1 docs.txt
python makematrix.py
python makeneighbour.py
# python cosine.py

# 作成したデータをarchiveに移す
mkdir archive/${DIR_DATE}
cp docs.txt archive/${DIR_DATE}
cp terms.txt archive/${DIR_DATE}
cp matrix.mat archive/${DIR_DATE}
cp neighbours.dat archive/${DIR_DATE}
#cp cosine.dat archive/${DIR_DATE}
cp load_mat.py archive/${DIR_DATE}
cp mylib.py archive/${DIR_DATE}


# 以下のプログラムが追加されていく？
# python lsi.py
# python isomap.py
# python lle.py
# python deeplearning.py

