# coding: utf-8
import numpy as np
from scipy import io

mat_file = io.loadmat('matrix.mat')
matrix   = mat_file['matrix']
relation = mat_file['relation']

# lil = matrix.tolil()
# for i in xrange(lil.shape[0]):
#     print relation[i]
#     print lil.rows(i)
#     print lil.data(i)
