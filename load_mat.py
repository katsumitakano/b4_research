# coding: utf-8
import numpy as np
import scipy as sp
from scipy import io

mat_file = io.loadmat('matrix.mat')
matrix   = mat_file['matrix']
terms = mat_file['terms']
terms = map(lambda t: t.rstrip(), terms) # 末尾の空白削除
