# coding: utf-8
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

if argc != 2:
    sys.stderr.write("Usage: Mainichi_to_xml.py 年度\n")
    sys.exit()

year    = argv[1] # xmlに変換したい年度

cabocha = CaboCha.Parser()
file_paths = getFileList("/volsys/amber/nlp/corpus/news_paper/" + year)

for path in file_paths:
    save_path = "corpus/Mainichi/%s/%s.xml" % (year, splitext(basename(path))[0])
    fw = codecs.open(save_path, "w", encoding="utf-8")
    fr = codecs.open(path, "r", encoding="euc-jp")
    for line in fr.readlines():
        if re.match(u"＼Ｔ２＼", line) != None:
            tree = cabocha.parse(line[4:].encode("utf-8")) # 最初の＼Ｔ２＼は除く
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
