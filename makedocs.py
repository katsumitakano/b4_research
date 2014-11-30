# coding: utf-8

# 『testdata』フォルダ内のファイル群から、
# 行列生成に使うファイルを作成する。
# 引数で読み込み先ディレクトリを変更することも可能。
#
# ファイル形式： 単語リストが1行ずつに書かれている
# ----------------------------------------
# 太郎,花子,一緒,駄菓子屋,寄る
# 天気予報,明日,晴れ,予報
# これ,良い,壷
# ----------------------------------------
#
# スクレイピングの対象となるファイルは、
# BCCWJ のM-XML/以下のファイルのような形式を持つ

import re
import os
import sys
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from mylib import measure_time
from mylib import getFileList

def getTermsLists_MXML(xml):
    """
    xmlから <paragraph> タグの中身だけ取得
    """
    rlist = [] # returnするリスト
    termlist = []
    soup = BeautifulStoneSoup(xml)
    # 名詞/動詞/形容詞の単語のみ抽出
    extraction = re.compile(u'名詞-(普通名詞|固有名詞)|動詞|形容詞')
    for paragraph in soup.findAll('paragraph'):
        for suw in paragraph.findAll('suw'): # TODO: この辺高速化(lxml使う？)
            if extraction.match(suw['pos']):
                termlist.append(suw['lemma']) # 原型を格納
        rlist.append( termlist )
        termlist = []

    return rlist


def getTermsLists_BNC(xml):
    """
    BNCのxmlから単語を抽出
    """
    rlist = []
    termlist = []
    soup = BeautifulStoneSoup(xml)
    for paragraph in soup.findAll('p'):
        if len(paragraph) < 10: continue
        for word in paragraph.findAll('w'):
            # 品詞名を取得
            pos = word['pos'] 
            if pos == 'VERB' or pos == 'SUBST': # VERB: 動詞, SUBST: 名詞
                termlist.append( word['hw'] ) # 単語の原型を取得
        rlist.append( termlist )
        termlist = []

    return rlist

def getTermsLists_Mainichi(xml):
    """
    Mainichiのxmlから単語を抽出
    """
    rlist = []
    termlist = []
    soup = BeautifulStoneSoup(xml)
    for sentence in soup.findAll('sentence'): # sentenceが段落に対応
        for tok in sentence.findAll('tok'):
            features = tok['feature'].split(',')
            hinshi  = features[0]
            bunrui1 = features[1]
            genkei  = features[6]
            if (hinshi in [u'名詞', u'動詞', u'形容詞']) and (bunrui1 not in[u'数', u'非自立']):
                if genkei != u"*":
                    termlist.append( genkei ) # 原型が存在すれば、それを抽出
                else:
                    termlist.append( tok.text ) # 無ければ表層系を使う
        rlist.append( termlist )
        termlist = []

    return rlist

@measure_time
def makedocs(dir_path='testdata/', corpus_kind='BCCWJ'):
    """
    一行毎に単語リストが書かれたファイルを準備
    @dir_path:  読み込むディレクトリ先
    @save_name: 保存するファイル名
    """
    save_name = 'docs.txt'
    if  os.path.isfile( save_name ):
        os.remove( save_name )
    wfile = open ( save_name, 'a' )

    # ファイル名の一覧を取得
    files = getFileList( dir_path )
    
    threshold = 10 # 最低単語数(極端に短い記事を省く)

    # コーパスを読み込む関数を選択
    if   corpus_kind == 'BCCWJ':
        getFunction = getTermsLists_MXML
    elif corpus_kind == 'BNC':
        getFunction = getTermsLists_BNC
    elif corpus_kind == 'MAI':
        getFunction = getTermsLists_Mainichi
    else:
        print "corpus_kind Error"
        sys.exit()

    # XMLファイルを読み込み、元となる文書ファイルを作成
    for filename in files:
        with open( filename, 'r') as f:
            xml = f.read()
        for tlist in getFunction(xml): # 指定された読み込み関数を使用
            if len(tlist) < threshold: continue # 抽出単語が少なすぎる場合は無視
            wfile.write(','.join(tlist).encode('utf_8') + '\n')
        # 進捗を表示
        print filename
    
    wfile.close()


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    # print getFileList(argv[1])
    if argc == 3:
        # 読み込むディレクトリ先と、
        # コーパスの種類を指定
        makedocs(dir_path=argv[1], corpus_kind=argv[2])
    else:
        # デフォルトの指定で実行
        makedocs()
