# 研究用プログラム
---

## プログラム一覧

### ソースコード
* makedocs.py   - 行列生成の元となるファイルを生成
* makematrix.py - 行列と単語関連付けファイルの生成
* cosine.py     - コサイン類似度を用いて単語間の類似度を測る
* (lsi.py)      - LSIを用いて単語間の類似度を測る
* (isomap.py)   - isomapを用いて単語間の類似度を測る
* (lle.py)      - lleを用いて単語間の類似度を測る
* (deeplearning.py) - deeplearningを用いて単語間の類似度を測る
* load_mat.py       - iPythonで作業する準備用（%run load_mat.py）

### 生成されるリソース
* docs.txt          - 行列生成の元となるファイル
* matrix.mat        - 行列ファイル(単語辞書も付属)
* cosine.txt	    - cosine.pyで生成された単語間の類似度ファイル

### ディレクトリ
* archive/      - 作成された行列ファイル置き場
* testdata/     - プログラムの動きを確認するためのテストデータ
* sandbox/      - 砂遊び

## makedocs.py [dir_path] [save_name}

BCCWJのM-XMLファイル群から行列生成の元となるファイルを作成する。
通常は現在のディレクトリにdocs.txtを生成する。
生成されるのは以下のような形式のファイルである。

```
太郎,花子,一緒,駄菓子屋,寄る
天気予報,明日,晴れ,予報
これ,良い,壷
経済,内閣総理大臣,する,発表
```

## makematrix.py [load_name] [save_name]

文脈ファイルから行列ファイルを生成する。
通常はdocs.txtからmatrix.txtを生成する。
行列ファイルは scipy.io.savemat を用いて保存され、
行列 matrix と単語リスト relation を持つ

## cosine.py [mat_name] [put_name]

行列ファイルから単語間の類似度を羅列したファイルを生成する。
通所はmatrix.matからcosine.txtを生成する。
numpy/scipyを用いて、なるべく処理の高速化を図っている。

## mylib.py

自分のよく使う関数とかをここに溜め込む
* measure_time: 関数の実行時間を測るデコレータ（process.logに書き出し）
