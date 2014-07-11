# プログラムの説明

## makeMaterialDocFromCXML.py
csamples以下のC-XML形式のファイル群から、文脈ファイルを生成
output: material_doc.txt

## makeMaterialTermsFromMXML.py
msamples以下のM-XML形式のファイル群から、単語リストファイルを生成
output: material_terms.txt

## makeMatrix.py
material_doc.txt から行列ファイルと単語ファイルを生成
output1: matrix.dat
output2: relation.dat

## similar.py
単語と単語の類似度を測る


# 生成されるファイル

## material_doc.txt
## material_terms.txt
## matrix.dat
## relation.dat