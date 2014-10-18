# coding: utf-8
import numpy as np
import scipy as sp
from scipy import io

mat_file = io.loadmat('matrix.mat')
matrix   = mat_file['matrix']
relation = mat_file['relation']

