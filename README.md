# 研究用プログラム
---

## プログラム一覧

* makedocs.py   - 行列生成の元となるファイルを生成
* makematrix.py - 行列と単語関連付けファイルの生成
* cosine.py     - コサイン類似度を用いて単語間の類似度を測る
* (lsi.py)      - LSIを用いて単語間の類似度を測る
* (isomap.py)   - isomapを用いて単語間の類似度を測る
* (lle.py)      - lleを用いて単語間の類似度を測る
* (deeplearning.py) - deeplearningを用いて単語間の類似度を測る

* docs.txt          - 行列生成の元となるファイル
* matrix.mat        - 行列ファイル
* matrix_rel.txt    - 単語関連付けファイル 

* archive/      - 作成された行列ファイル置き場
* testdata/     - プログラムの動きを確認するためのテストデータ
* sandbox/      - 砂遊び

## makedocs.py

docs.txtを生成する
以下のような形式のファイル
```
太郎,花子,一緒,駄菓子屋,寄る
天気予報,明日,晴れ,予報
これ,良い,壷
```

## makematrix.py

matrix.matとmatrix_rel.txtを生成する
matrix.matはバイナリファイル
matrix_rel.txtはpickle化されたファイル

