import numpy as np
from se3 import vec_to_se3, matrix_exp6

def FkinSpace(SList, ThetaList, M):
    T = np.eye(4)
    length = len(ThetaList)
    for i in range (length - 1):
        T = T @ matrix_exp6(vec_to_se3(SList[:,i] * ThetaList[i]))
    T = T @ M
    T[0,3] = T[0,3] #+ 0.102
    return T
       