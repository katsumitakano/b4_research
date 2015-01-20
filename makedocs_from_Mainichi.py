# coding: utf-8
# 毎日新聞のテキストから\T2\の部分だけ抽出し、
# 段落単位または文単位の文章ファイルを生成する

import os
import re
import sys
import codecs
import MeCab
from mylib import measure_time
from mylib import getFileList

mecab = MeCab.Tagger()

def mecab_parser(text):
    """テキストから必要な単語だけを抽出し、リストを返す"""

    termlist = []
    node = mecab.parseToNode(text)
    while node != None:
        surface = node.surface
        feature = node.feature.split(',')
        hinshi = feature[0]
        bunrui = feature[1]
        genkei = feature[6]
        if (hinshi in ['名詞', '動詞', '形容詞']) and \
           (bunrui not in['数', '非自立']):
            if genkei != "*":
                termlist.append( genkei )
            else:
                termlist.append( surface )
        node = node.next

    return termlist

@measure_time
def makedocs(corpus_dir, kind):
    """docs.txtファイルの作成"""

    save_name = 'docs.txt'
    fw = codecs.open (save_name, 'w', encoding="utf-8")

    file_paths = getFileList(corpus_dir)
    termlist = []
    for path in file_paths:
        fr = codecs.open(path,  "r", encoding="euc-jp")
        for line in fr.readlines():
            if re.match(u"＼Ｔ２＼", line) != None:
                line = line[4:].strip()       # 最初の＼Ｔ２＼は除く
                sentences = line.split(u'。') # 文単位に区切る

                """ --- 段落単位にするか、文単位にするか場合分け --- """
                if kind == "-s":
                    for sen in sentences:
                        sen = sen + u"。"     # 一応、句点を足す
                        termlist = mecab_parser(sen.encode("utf-8"))
                        if termlist != []:
                            fw.write(','.join(termlist).decode('utf_8') + '\n')
                            termlist = []
                elif kind == "-p":
                    for sen in sentences:
                        sen = sen + u"。"     # 一応、句点を足す
                        termlist.extend( mecab_parser(sen.encode("utf-8")) )
                    if termlist != []:
                        fw.write(','.join(termlist).decode('utf_8') + '\n')
                        termlist = []

        print path # 進捗確認

    fw.close()
    fr.close()


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    # エラー処理
    if argc != 3:
        sys.stderr.write("Usage: makedocs_from_Mainichi.py ディレクトリ名 [-p|-s]\n")
        sys.exit()
    elif argv[2] not in ["-p", "-s"]:
        sys.stderr.write("Usage: makedocs_from_Mainichi.py ディレクトリ名 [-p|-s]\n")
        sys.exit()

    corpus_dir = argv[1] # 読み出すディレクトリ名
    kind       = argv[2] # タイプ（段落 or 文）

    makedocs(corpus_dir, kind)
