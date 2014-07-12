# coding: utf-8
# 対象ファイルは material_terms.txt

import os

def makeMatrix():
    """
    material_terms.txt からCoordinate形式の行列を作成する
    """
    if os.path.isfile( 'coordinateMatrix.dat' ):
        os.remove( 'coordinateMatrix.dat' )
    
    f_matrix   = open( 'coordinateMatrix.dat', 'a' )

    # 重複の無い単語リストを生成
    uniterms = set()
    for line in open( 'material_terms.txt'):
        uniterms = uniterms | set(line.split(','))

    p = 0
    # Coordinate形式の疎行列を生成
    for j, line in enumerate(open( 'material_terms.txt' )):
        for i, term in enumerate(uniterms):
            val = line.split(',').count( term )
            if val:
                f_matrix.write("%d %d %f\n" % (i, j, val))

        print p # 進捗確認
        p += 1

    f_matrix.close()


if __name__ == "__main__":
    makeMatrix()


#------------------------テスト -----------------------------
def test():
    pass
