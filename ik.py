import numpy as np
from se3 import se3_to_vec, matrix_log6
from fk import FkinSpace
from jacobian import jacobian_space

def analytic_ik(xcalc,y,z,L1,L2,L3):
    x = xcalc - 0.0693
    r = np.sqrt(x**2 + y**2)
    theta1 = np.atan2(y,x)

    z = z-L1
    r2 = np.sqrt(z**2 + r**2)

    theta2 = np.acos((L2**2 + r2**2 - L3**2) / (2*L2*r2))

    beta = np.acos((L2**2 + L3**2 - r2**2) / (2 * L2*L3))
    theta3 = np.pi - beta

    return theta1,theta2,theta3

def IKinSpace(SList, M, Tsd, ThetaList0, eomg, ev, maxiter):
    thetaList = ThetaList0.copy()
    for i in range (maxiter):
        Tsb = FkinSpace(SList, thetaList, M)
        Tbd = np.linalg.inv(Tsb) @ Tsd
        Vb = se3_to_vec(matrix_log6(Tbd))
        err_omg = np.linalg.norm(Vb[0:3])
        err_v = np.linalg.norm(Vb[3:6])
        if(err_v < ev and err_omg < eomg):
            return thetaList,True
        J = jacobian_space(SList, thetaList)
        thetaList += np.linalg.pinv(J, rcond=1e-4) @ Vb
    return thetaList, False