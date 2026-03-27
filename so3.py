import numpy as np

def skew(v):
    return np.array([[0,-v[2],v[1]],
                    [v[2],0,-v[0]],
                    [-v[1],v[0],0]])

def vec_to_so3(v):
    return skew(v)

def so3_to_vec(so3):
    return np.array([so3[2,1], so3[0,2], so3[1,0]])

def matrix_exp3(so3):
    omega = so3_to_vec(so3)
    theta = np.linalg.norm(omega)
    if(theta < 1e-6):
        return np.eye(3)
    omegahat = so3 / theta
    return(
        np.eye(3) + np.sin(theta) * omegahat + (1 - np.cos(theta)) * np.dot(omegahat, omegahat)
    )

def matrix_log3(R):
    acos_input = (np.trace(R)-1)/2.0
    theta = np.arccos(np.clip(acos_input, -1, 1))
    if abs(theta) < 1e-6:
        return np.zeros((3,3))
    return theta / (2 * np.sin(theta)) * (R - R.T)