# coding: utf-8

# 『dsamples』フォルダ内のファイル群から、
# 行列生成に使うファイルを作成する。
# ファイル形式： 文脈が1行ずつに書かれている（文、文章を問わない）
#
# ----------------------------------------
# 太郎は花子と一緒に帰った。帰りに駄菓子屋に寄った。
# 天気予報で明日は晴れるとの予報があった。
# これは良い壷だ！
# ----------------------------------------
#
# スクレイピングの対象となるファイルは、
# BCCWJ のC-XML/以下のファイルのような形式を持つ

import re
import os
from BeautifulSoup import BeautifulSoup


def getParagraphsFromXml(xml):
    """
    xmlから <paragraph> タグの中身だけ取得
    """
    p = re.compile(r'<.*?>')
    q = re.compile(r'(\n|\r|　)')
    soup = BeautifulSoup(xml)
    rlist = []
    for para in soup.findAll('paragraph'):
        text = str(para)
        text = p.sub("", text)
        text = q.sub("", text)
        rlist.append( text )

    return rlist


def main(save_file = 'material_doc.txt'):
    """
    一行毎に文脈が書かれたファイルを準備
    @save_file: 保存するファイル名
    """
    if  os.path.isfile( save_file ):
        os.remove( save_file )
    wfile = open ( save_file, 'a' )

    direc = "./csamples"
    files = os.listdir(direc)

    p = 1
    for _file in files:
        _file = os.path.join(direc, _file)
        with open( _file, 'r') as f:
            xml = f.read()
        for l in getParagraphsFromXml(xml):
            wfile.write(l+'\n')
        # 進捗を表示
        print p
        p += 1
    
    wfile.close()


if __name__ == "__main__":
    main()


#------------------------テスト -----------------------------
def test():
    direc = "/export/home/jade/katsumi/corpus/C-XML/VARIABLE/PN/PN"
    files = os.listdir(direc)

    for _file in files:
        _file = os.path.join(direc, _file)
        with open( _file, 'r') as f:
            xml = f.read()
        for l in getParagraphsFromXml(xml):
            print l
