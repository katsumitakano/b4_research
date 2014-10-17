# coding: utf-8
import numpy as np
import scipy as sp

mat_file = sp.io.loadmat('matrix.mat')
matrix   = mat_file['matrix']
relation = mat_file['relation']

