#!/bin/sh
# $1: 読み込むXMLファイルのあるディレクトリ
# $2: コーパスの種類を選択
# $3: 最低単語数

# 行列の作成と類似度の計算
python makedocs.py $1 $2
python makematrix.py $3
python makeneighbour.py
python maketable.py
python svd.py 300

# 作成した行列の情報をinfo.txtに書き込む
touch info.txt
: > info.txt
echo "corpus:"$1 >> info.txt
echo "kind:"$2 >> info.txt
echo "threshold:"$3 >> info.txt
wc -l terms.txt >> info.txt
wc -l docs.txt >> info.txt

# 移動するファイル群
MOVE_FILE=(
"docs.txt"
"terms.txt"
"eval_sigeki.txt"
"eval_all.txt"
"eval_data.pkl"
"matrix.mat"
"neighbours.dat"
"load_mat.py"
"research.py"
"isomap.py"
"lle.py"
"svd.py"
"svd_d300.mat"
"check_terms.py"
"mylib.py"
"info.txt")

# ディレクトリ名に使用
DIR_DATE=`date +"%m%d_%H%M%S"`

# 作成したデータをarchiveに移す
mkdir archive/${DIR_DATE}
for FILE in "${MOVE_FILE[@]}"
do
    cp $FILE archive/${DIR_DATE}
done
