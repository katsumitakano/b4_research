# coding: utf-8
import numpy as np
import scipy as sp
from sklearn import manifold

mat_file = sp.io.loadmat('matrix.mat')
matrix   = mat_file['matrix']
relation = mat_file['relation']

isomap = manifold.Isomap()
lle = manifold.LocallyLinearEmbedding()

# Y = isomap.fit_transform(matrix.toarray())
