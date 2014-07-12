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
import time
import datetime
from BeautifulSoup import BeautifulSoup


def getTermsListsFromXml(xml):
    """
    xmlから <paragraph> タグの中身だけ取得
    """
    soup = BeautifulSoup(xml)
    rlist = []
    termlist = []
    for paragraph in soup.findAll('paragraph'):
        for luw in paragraph.findAll('luw'): # TODO: この辺高速化(lxml使う？)
            if re.match(u'名詞|動詞', luw['l_pos']): # 名詞または動詞の単語のみ抽出
                termlist.append(luw['l_lemma'])
        rlist.append( termlist )
        termlist = []

    return rlist


def main(save_file = 'material_terms.txt'):
    """
    一行毎に単語リストが書かれたファイルを準備
    @save_file: 保存するファイル名
    """
    if  os.path.isfile( save_file ):
        os.remove( save_file )
    wfile = open ( save_file, 'a' )

    direc = "./msamples"
    files = os.listdir(direc)

    p = 1
    for _file in files:
        _file = os.path.join(direc, _file)
        with open( _file, 'r') as f:
            xml = f.read()
        for l in getTermsListsFromXml(xml):
            wfile.write(','.join(l).encode('utf_8') + '\n')
        # 進捗を表示
        print p
        p += 1
    
    wfile.close()


if __name__ == "__main__":

    start = time.time()
    main()
    end = time.time()
    with open('process.log', 'a') as f:
        log = "%s %s %f sec\n" % (str(datetime.datetime.now()), __file__, (end - start))
        f.write( log )


#------------------------テスト -----------------------------
def test():
    pass
