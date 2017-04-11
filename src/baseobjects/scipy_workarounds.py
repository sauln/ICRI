import numpy as np
from itertools import product

def pdist(mat):
    res = np.zeros(mat.shape)
    for x,y in product(range(mat.shape[0]), range(mat.shape[1])):
        res[x][y] = np.linalg.norm(mat[x] - mat[y])

    return res

