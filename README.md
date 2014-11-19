# 研究用プログラム
各ファイルの役割とか、簡単な使い方とかをまとめてあります。

## 使い方
基本的な流れとして、まず make.sh に引数を与えて実行します。
引数にはBCCWJのM-XML形式のコーパスを指定します。
```
./make.sh /volsys/amber/nlp/BCCWJ/disk1/M-XML/PN/PN
```

様々なファイルが生成されますが、matrix.matが一番重要なファイルです。
この後、isomap.pyやlle.pyを用いてそれぞれの意味空間を作成します。
```
python isomap.py 6 200
python lle.py 4 200
python svd 200
```

意味空間が作成できたら、research.pyで意味空間の探索が行えます。
```
python research.py
Input matrix name (***.mat) -> svd_d200.mat
terms? -> 総理
コイズミ 0.862873733439
大臣 0.837900125451
ナガタチョウ 0.825307572232
政局 0.824343865183
野党 0.818585020051
首相 0.79551960604
解散 0.789710932078
造反 0.785865243498
カメイ 0.774857267016
総裁 0.773829276498
terms? -> 総理　車
0.00266860434679
terms? -> ...
```

最後に評価を行います…（そのうち書く）

## プログラム一覧

### ソースコード
* makedocs.py	- 行列生成の元となるファイルを生成
* makematrix.py	- 行列と単語関連付けファイルの生成
* makeneighbour.py	- 近傍点を格納したファイルを生成
* cosine.py     - コサイン類似度を用いて単語間の類似度を測る
* isomap.py	- Isomapで次元圧縮した行列ファイルを生成
* lle.py	- LocallyLinearEmbeddingで次元圧縮した行列ファイルを生成
* svd.py	- SVDで次元圧縮した行列ファイルを生成
* load_mat.py	- iPythonで作業する準備用（%ipython -i load_mat.py）
* research.py	- 次元圧縮後の意味空間を探索する
* mylib.py	- 自作の便利関数郡
* make.sh	- コーパスから意味空間を作成する一連のプログラムを実行
* clear.sh	- Emacsの一時ファイル（.~）を削除

### 生成されるリソース
* docs.txt	- 行列生成の元となるファイル
* terms.txt	- 行列に含まれる全単語を並べたファイル
* matrix.mat	- 行列ファイル(単語辞書も付属)
* neighbours.dat  - makeneighbour.pyで生成された近傍点のファイル
* cosine.dat	  - cosine.pyで生成された単語間の類似度ファイル
* P_isomap.npy	  - Isomapで固有値計算する前の行列（計算用に使用）
* M_lle.npy	  - LocallyLinearEmbeddingで固有値計算する前の行列（計算用に使用）
* process.log	  - プログラムの実行時間などが保存されるログファイル

### ディレクトリ
* archive/	- 作成された行列ファイル置き場
* eval_data/	- 意味空間の評価に使う連想語の分類データ
* testdata/	- プログラムの動きを確認するためのテストデータ
* sandbox/	- 砂遊び


## プログラムの詳細
### makedocs.py [dir_path] [save_name}

BCCWJのM-XMLファイル群から行列生成の元となるファイルを作成する。
通常は現在のディレクトリにdocs.txtを生成する。
生成されるのは以下のような形式のファイルである。

```
太郎,花子,一緒,駄菓子屋,寄る
天気予報,明日,晴れ,予報
これ,良い,壷
経済,内閣総理大臣,する,発表
```

### makematrix.py [load_name] [save_name]

文脈ファイルから行列ファイルを生成する。
通常はdocs.txtからmatrix.txtを生成する。
行列ファイルは scipy.io.savemat を用いて保存され、
行列 matrix と単語リスト terms を持つ

### makeneighbour.py

近傍点ファイルneighbours.datを作成する。

### cosine.py [mat_name] [put_name]

行列ファイルから単語間の類似度を羅列したファイルを生成する。
通所はmatrix.matからcosine.txtを生成する。
numpy/scipyを用いて、なるべく処理の高速化を図っている。

### isomap.py k=近傍点 d=圧縮後の次元 [test]

圧縮後のmatファイルをisomap_k{}_d{}.matに書き出す。
testを指定すると動きを確認できる。

### lle.py k=近傍点 d=圧縮後の次元 [test]

圧縮後のmatファイルをlle_k{}_d{}.matに書き出す
testを指定すると動きを確認できる。

### svd.py d=圧縮後の次元
圧縮後のmatファイルをsvd_d{}.matに書き出す

### make.sh コーパスのディレクトリ
意味空間元となる行列を作成するために、一連のプログラムを実行する

### mylib.py

自分のよく使う関数とかをここに溜め込む
* measure_time: 関数の実行時間を測るデコレータ（process.logに書き出し）
* getFileList: 指定したディレクトリ以下の全ファイルへのパスを,リスト形式で返却
* plot3d: 3次元プロット
* plot2d: 2次元プロット