import numpy as np
from se3 import matrix_exp6,vec_to_se3,adjoint

def jacobian_space(SList, ThetaList):
    n = len(ThetaList)
    Js = np.zeros((6,n))
    Js[:,0] = SList[:,0]
    T = np.eye(4)
    for i in range (1,n):
        T = T @ matrix_exp6(vec_to_se3(SList[:, i-1] * ThetaList[i-1]))
        Js[:,i] = adjoint(T) @ SList[:,i]
    return Js