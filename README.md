# 研究用プログラム
各ファイルの役割とか、簡単な使い方とかをまとめてあります。

## 使い方
基本的な流れとして、まず make.sh に引数を与えて実行します。
引数にはコーパスのディレクトリ、コーパスの種類、最低単語数を指定します。
**でも恐ろしく時間がかかるから気軽に実行しないほうがいい。
プログラムの実行手順を確認して、個別に実行したほうが無難。**
```
$ ./make.sh /volsys/amber/nlp/BCCWJ/disk1/M-XML/PN/PN BCCWJ 20
```

様々なファイルが生成されますが、matrix.matが一番重要なファイルです。
この後、isomap.pyやlle.pyを用いてそれぞれの意味空間を作成します。
```
$ python isomap.py -k 6 200
$ python isomap.py -r 8 200
$ python lle.py 4 200
$ python svd 200
```

意味空間が作成できたら、research.pyで意味空間の探索が行えます。
:c[osine]と:e[uclid]で距離計算の方法を変更できます。
```
$ python research.py svd_d200.mat
Matfile loaded!
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
terms? -> :e
Change simType to "euclid"
terms? -> ...
```

最後にevaluate.pyで意味空間の評価を行います（eval_data.pklが必要です）。
```
$ python evaluate svd_d300.mat
idiom_Rate.dat
0.42099061847
co_exist_Rate.dat
0.493707107843
syntactic_Rate.dat
0.375587214052
part_of_Rate.dat
0.467864923747
member_of_Rate.dat
0.527350562867
synonym_Rate.dat
0.610165118679
antnym_Rate.dat
0.647058823529
same_member_Rate.dat
0.485294117647
```

引数に評価を行う行列ファイルの名前を与えると、各関係での評価値を出してくれます。
基本はF値を出力しますが、再現率を見たい場合はプログラムの中身を書き換えて下さい。

## プログラム一覧

### ソースコード
* make.sh	- コーパスから意味空間を作成する一連のプログラムを実行
* makedocs.py	- 行列生成の元となるファイルを生成
* makedocs_from_Mainichi.py	- 毎日新聞コーパスから直接文書ファイルを生成する
* makeCOmatrix.py	- 共起頻度行列の生成
* makeTFmatrix.py	- 単語文脈行列の生成
* makeneighbour.py	- 近傍点を格納したファイルを生成
* maketable.py		- 評価に使う表形式のデータ（＋α）を生成
* isomap.py	- Isomapで次元圧縮した行列ファイルを生成
* lle.py	- LocallyLinearEmbeddingで次元圧縮した行列ファイルを生成
* svd.py	- SVDで次元圧縮した行列ファイルを生成
* check_terms.py  - 評価に使う単語の中から意味空間に含まれていない単語を出力
* evaluate.py	- 意味空間の評価を行うプログラム
* research.py	- 次元圧縮後の意味空間を探索する
* generator.py	- 固有値と固有ベクトルのファイルから次元数の異なる行列を生成する
* mylib.py	- 自作の便利関数郡
* load_mat.py	- iPythonで作業する準備用（%ipython -i load_mat.py）

### ソースコード（ほぼ使ってない）
* clear.sh	- Emacsの一時ファイル（.~）を削除
* cosine.py     - コサイン類似度を用いて単語間の類似度を測る
* denseEigSolver.cpp	- Eigenを使用した固有値分解（Pythonより遅かった）


### 生成されるリソース
* docs.txt	- 行列生成の元となるファイル
* terms.txt	- 行列に含まれる全単語を並べたファイル
* matrix_co.mat	- 共起頻度行列のファイル(単語辞書も付属)
* matrix_tf.mat	- 単語文脈行列のファイル(単語辞書も付属)
* neighbours.dat  - makeneighbour.pyで生成された近傍点のファイル
* eval_data.pkl	  - 秋山さんの分類データを表形式にまとめたもの
* eval_sigeki.txt - 分類データのうちの刺激語
* eval_all.txt	  - 分類データの全単語（刺激語も含む）
* cosine.dat	  - cosine.pyで生成された単語間の類似度ファイル
* process.log	  - プログラムの実行時間などが保存されるログファイル
* info.txt	  - 意味空間の情報を記述（コーパスの種類、最低単語数、単語数、文脈数）
* (P_isomap.npy	  - Isomapで固有値計算する前の行列（計算用に使用）)
* (M_lle.npy	  - LocallyLinearEmbeddingで固有値計算する前の行列（計算用に使用）)


### ディレクトリ
* archive/	- 作成された行列ファイル置き場
* corpus/	- コーパス置き場
* eval_data/	- 意味空間の評価に使う連想語の分類データ
* testdata/	- プログラムの動きを確認するためのテストデータ
* sandbox/	- 砂遊び


## プログラムの詳細
**あまりドキュメントを整備してない。**   
**ソースコードの中身読んだほうが確実。**

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
