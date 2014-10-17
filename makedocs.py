# coding: utf-8

# 『msamples』フォルダ内のファイル群から、
# 行列生成に使うファイルを作成する。
# ファイル形式： 単語リストが1行ずつに書かれている
#
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
import time
import datetime
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from mylib import measure_time
from mylib import getFileList

def getTermsLists(xml):
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

    # あとで書く
    return rlist


@measure_time
def makedocs(dir_path='testdata/', save_name='docs.txt'):
    """
    一行毎に単語リストが書かれたファイルを準備
    @dir_path:  読み込むディレクトリ先
    @save_name: 保存するファイル名
    """
    if  os.path.isfile( save_name ):
        os.remove( save_name )
    wfile = open ( save_name, 'a' )

    # ファイル名の一覧を取得
    files = getFileList( dir_path )
    
    threshold = 5 # 最低単語数
    for filename in files:
        with open( filename, 'r') as f:
            xml = f.read()
        #for tlist in getTermsLists_BNC(xml): #BNC用
        for tlist in getTermsLists(xml):
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
        # 保存時のファイル名を指定
        makedocs(dir_path=argv[1], save_name=argv[2])
    else:
        # デフォルトの指定で実行
        makedocs()
