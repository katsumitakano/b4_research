# coding: utf-8
import os
import sys
import codecs
import numpy as np
from scipy import io as spio
from subprocess import call

argv = sys.argv
argc = len(argv)

if argc != 3:
    sys.stderr.write('Usage: python generator.py 固有値 固有ベクトル')
    sys.exit()

eval_file = argv[1]             # 固有値ファイル
evec_file = argv[2]             # 固有値ベクトルファイル

kind  = eval_file[0:-4].split('_')[0] # ファイル名から種類を取得
param = eval_file[0:-4].split('_')[2] # ファイル名からパラメータだけ取得

_kind_chk  = evec_file[0:-4].split('_')[0] # チェック用
_param_chk = evec_file[0:-4].split('_')[2] # チェック用


# --- エラー処理
if kind not in ['isomap', 'lle']:
    sys.stderr.write('Usage: python generator.py 種類[isomap|lle] 固有値 固有ベクトル')
    sys.exit()
elif kind != _kind_chk: 
    sys.stderr.write('Error: Use same Kind.\n')
    sys.exit()
elif param != _param_chk:
    sys.stderr.write('Error: Use same Param.\n')
    sys.exit()


# --- データの読み込み
evals = np.load(eval_file)
evecs = np.load(evec_file)
terms = spio.loadmat('matrix_co.mat')['terms']


# --- 保存用のディレクトリを作成
dir_name = "%s_%s" % (kind, param)
try:
    os.mkdir(dir_name)
except OSError:
    sys.stderr.write("OK. Directory is Exist.\n")

# 種類に合わせて圧縮用の関数を切り替え
if   kind == 'isomap':
    def compress(dim):
        W = evals[:dim]
        X = evecs[:,:dim]
        return np.sqrt(W)*X # dim個の固有値と固有ベクトルの積

elif kind == 'lle':
    def compress(dim):
        return evecs[:,:dim] # dim個の固有ベクトル

# --- 複数次元の意味空間を生成
for dim in xrange(50, 310, 10):
    save_name = "%s_%s_d%s" % (kind, param, dim)
    Y = compress(dim)
    spio.savemat(dir_name+'/'+save_name, {'Y':Y, 'terms':terms})
    print "genarating %s" % (save_name)
