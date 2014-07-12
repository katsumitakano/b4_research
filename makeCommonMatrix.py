# coding: utf-8
# 対象ファイルは BCCWJ のC-XML/以下のファイル群

import os
import MeCab
from BeautifulSoup import BeautifulSoup

def parseToIndep(article):
    """
    与えられたテキストを形態素で分解し、
    自立語（名詞と動詞）のリストを返す
    """
    mecab = MeCab.Tagger()
    node = mecab.parseToNode(article)
    
    result = []
    while node != None:
        feature = node.feature.split(',')
        # 名詞または動詞の時のみappend
        if feature[0] == "名詞" or feature[0] == "動詞":
            result.append(node.surface)
        node = node.next

    return result


def docsToMatrix(doclist):
    """
    文書群のリストから単語・文書行列を生成する
    """
    parsed_lists = [parseToIndep(doc) for doc in doclist]

    # 重複の無い単語リストを生成
    non_repeated = set([])
    for vec in parsed_lists:
        non_repeated = non_repeated.union(vec)
        
    # それぞれの単語に対し、文書での出現数を数える
    term_matrix = {}
    for word in non_repeated:
        term_matrix[word] = [str(v.count(word)) for v in parsed_lists]

    return term_matrix


def makeMatrix():
    """
    material_doc.txt から単語文脈行列を作成する
    """
    if os.path.isfile( 'matrix.dat' ):
        os.remove( 'matrix.dat' )
    if os.path.isfile( 'relation.dat' ):
        os.remove( 'relation.dat' )
    
    f_matrix   = open( 'matrix.dat', 'a' )
    f_relation = open( 'relation.dat', 'a' )

    with open( 'material_doc.txt', "r") as f:
        mycorpus = f.readlines()
    
    print("done1")
    term_matrix = docsToMatrix(mycorpus)

    print("done2")
    line_counter = 0
    for term, vector in term_matrix.items():
        f_matrix.write( ' '.join(vector) + '\n' )
        f_relation.write( term + ' ' + str(line_counter)+ '\n' )
        line_counter += 1
        print( line_counter )   # 進捗確認

    f_matrix.close()
    f_relation.close()


if __name__ == "__main__":
    makeMatrix()


#------------------------テスト -----------------------------
def test():
    pass
