#!/bin/sh
# $1: 読み込むXMLファイルのあるディレクトリ
# $2: コーパスの種類を選択
# $3: 最低単語数

# 行列の作成と類似度の計算
python makedocs.py $1 $2
python makeCOmatrix.py $3
cp terms.txt terms_co.txt
python makeTFmatrix.py $3
cp terms.txt terms_tf.txt
python makeneighbour.py
python maketable.py
python svd.py 300

# 作成した行列の情報をinfo.txtに書き込む
touch info.txt
: > info.txt
echo "corpus:"$1 >> info.txt
echo "kind:"$2 >> info.txt
echo "threshold:"$3 >> info.txt
echo "terms_co" >> info.txt
wc -l terms_co.txt >> info.txt
echo "terms_tf" >> info.txt
wc -l terms_tf.txt >> info.txt
wc -l docs.txt >> info.txt

# 移動するファイル群
MOVE_FILE=(
"docs.txt"
"terms_co.txt"
"terms_tf.txt"
"evaluate.py"
"eval_sigeki.txt"
"eval_all.txt"
"eval_data.pkl"
"matrix_co.mat"
"matrix_tf.mat"
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
