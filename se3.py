from so3 import vec_to_so3, so3_to_vec, matrix_exp3, matrix_log3
import numpy as np

def vec_to_se3(v):
    se3 = np.zeros((4,4))
    w = v[0:3]
    v = v[3:]
    se3[0:3,0:3] = vec_to_so3(w)
    se3[0:3,3] = v
    return se3

def se3_to_vec(se3):
    vec = np.zeros((6))
    vec[0:3] = so3_to_vec(se3[0:3,0:3])
    vec[3:6] = se3[0:3,3]
    return vec

def matrix_exp6(se3):
    omega = se3[0:3,0:3]
    v = se3[0:3,3]
    theta = np.linalg.norm(so3_to_vec(omega))
    if(theta < 1e-6):
        T = np.eye(4)
        T[0:3,3] = v
        return T
    omegahat = omega / theta
    R = matrix_exp3(omega)
    G = (np.eye(3) * theta + (1 - np.cos(theta)) * omegahat + (theta - np.sin(theta)) * np.dot(omegahat, omegahat))
    P = np.dot(G, v/theta)
    T = np.eye(4)
    T[0:3,0:3] = R
    T[0:3,3] = P
    return T

def matrix_log6(T):
    R = T[0:3,0:3]
    p = T[0:3,3]
    omgmat = matrix_log3(R)
    omega = so3_to_vec(omgmat)
    if(np.linalg.norm(omega) < 1e-6):
        se3mat = np.zeros((4,4))
        se3mat[0:3,3] = p
        return se3mat

    theta = np.linalg.norm(omega)
    omgmat_unit = omgmat / theta
    G_inv = (np.eye(3) / theta - 0.5 * omgmat_unit + (1/theta - 0.5 / np.tan(theta / 2)) * (omgmat_unit @ omgmat_unit))
    v = G_inv @ p
    se3mat = np.zeros((4,4))
    se3mat[0:3,0:3] = omgmat
    se3mat[0:3, 3] = v * theta
    return se3mat


def adjoint(T):
    R = T[0:3,0:3]
    p = T[0:3,3]
    skewp = vec_to_so3(p)
    adT = np.zeros((6,6))
    adT[0:3,0:3] = R
    adT[3:6, 3:6] = R
    adT[3:6, 0:3] = skewp @ R
    return adT


def ad(V):

    w = V[:3]
    v = V[3:]

    adV = np.zeros((6,6))

    adV[:3,:3] = vec_to_so3(w)
    adV[3:,3:] = vec_to_so3(w)
    adV[3:,:3] = vec_to_so3(v)

    return adV