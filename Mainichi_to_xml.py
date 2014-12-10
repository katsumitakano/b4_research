# coding: utf-8
# 毎日新聞コーパスからCabochaを使ってXMLファイルを作成
# ※かなり殴り書き、ファイルの後始末とかダメかもしれない

import os
import re
import sys
import codecs
import MeCab
import CaboCha
from os.path import splitext, basename
from mylib import getFileList

argv = sys.argv
argc = len(argv)

if argc != 3:
    sys.stderr.write("Usage: Mainichi_to_xml.py 年度 種類[-p|-s]\n")
    sys.exit()

year    = argv[1] # xmlに変換したい年度
kind    = argv[2] # xmlのタイプ（段落or文）

# タイプのチェック
if kind not in ["-p", "-s"]:
    sys.stderr.write("Usage: Mainichi_to_xml.py 年度 種類[-p|-s]\n")
    sys.exit()

# --- タイプに従い記事をパース --------------------------------------------

cabocha = CaboCha.Parser()
file_paths = getFileList("/volsys/amber/nlp/corpus/news_paper/" + year)

# 段落単位でパース
if kind == '-p':
    for path in file_paths:
        save_path = "corpus/Mainichi/%s_p/%s.xml" % (year, splitext(basename(path))[0])
        fw = codecs.open(save_path, "w", encoding="utf-8")
        fr = codecs.open(path, "r", encoding="euc-jp")
        for line in fr.readlines():
            if re.match(u"＼Ｔ２＼", line) != None:
                tree = cabocha.parse(line[4:].encode("utf-8")) # 最初の＼Ｔ２＼は除く
                results = tree.toString(CaboCha.FORMAT_XML)
                fw.write(results.decode("utf-8"))
        # 進捗確認
        sys.stderr.write(path+"\n")

# 文単位でパース
elif kind == '-s':
    for path in file_paths:
        save_path = "corpus/Mainichi/%s_s/%s.xml" % (year, splitext(basename(path))[0])
        fw = codecs.open(save_path, "w", encoding="utf-8")
        fr = codecs.open(path, "r", encoding="euc-jp")
        for line in fr.readlines():
            if re.match(u"＼Ｔ２＼", line) != None:
                sentences = line[4:].rstrip().split(u"。") # 句点で分割
                for sen in sentences:
                    sen = sen+u"。" # 句点を足す
                    tree = cabocha.parse(sen.encode("utf-8"))
                    results = tree.toString(CaboCha.FORMAT_XML)
                    fw.write(results.decode("utf-8"))
        # 進捗確認
        sys.stderr.write(path+"\n")

fw.close()
fr.close()



# ---------------------------------------------------------------
# text = "太郎は花子に二郎の本を貸した。"

# MeCabのサンプル
# mecab = MeCab.Tagger()
# node = mecab.parseToNode(text)

# while node != None:
#     surface = node.surface
#     feature = node.feature.split(',')
#     print surface + "\t" + ', '.join(feature)

#     node = node.next

# CaboChaのサンプル
# cabocha = CaboCha.Parser()
# tree = cabocha.parse(text)

# results = tree.toString(CaboCha.FORMAT_XML)
# print results
