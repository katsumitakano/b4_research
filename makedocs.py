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
from mylib import measure_time


def getTermsLists(xml):
    """
    xmlから <paragraph> タグの中身だけ取得
    """
    soup = BeautifulSoup(xml)
    rlist = []
    termlist = []
    for paragraph in soup.findAll('paragraph'):
        for luw in paragraph.findAll('luw'): # TODO: この辺高速化(lxml使う？)
            if re.match(u'名詞|動詞|形容詞', luw['l_pos']): # 名詞/動詞/形容詞の単語のみ抽出
                termlist.append(luw['l_lemma'])
        rlist.append( termlist )
        termlist = []

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
    files = os.listdir( dir_path )

    for p, filename in enumerate(files):
        filename = os.path.join(dir_path, filename)
        with open( filename, 'r') as f:
            xml = f.read()
        for tlist in getTermsLists(xml):
            if tlist == []: continue # 単語抽出出来なかった時は書き込まない
            wfile.write(','.join(tlist).encode('utf_8') + '\n')
        # 進捗を表示
        print p
    
    wfile.close()


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    if argc == 3:
        # 読み込むディレクトリ先と、
        # 保存時のファイル名を指定
        makedocs(argv[1], argv[2])
    else:
        # デフォルトの指定で実行
        makedocs()
