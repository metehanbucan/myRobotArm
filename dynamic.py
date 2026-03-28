import numpy as np
from se3 import adjoint, vec_to_se3, matrix_exp6, ad
import matplotlib.pyplot as plt

def recursive_newton_euler_algorithm(SList, MList, GList, theta, thetadot, thetaddot, g):
    n = len(theta)
    AList = [np.zeros(6) for _ in range (n+1)]
    T = np.eye(4)
    for i in range(n):
        T = T @ MList[i]
        A = adjoint(np.linalg.inv(T)) @ SList[:,i]
        AList[i] = A

    AdTi = [None]*(n+1)
    V = [np.zeros(6) for _ in range (n+1)]
    Vd = [np.zeros(6) for _ in range(n+1)]

    Vd[0][3:] = -g

    for i in range (n):
        T = matrix_exp6(vec_to_se3(-AList[i] * theta[i])) @ np.linalg.inv(MList[i])
        AdTi[i] = adjoint(T)
        V[i+1] = AdTi[i] @ V[i] + AList[i] * thetadot[i]
        Vd[i+1] = AdTi[i] @ Vd[i] + ad(V[i+1]) @ (AList[i] * thetadot[i]) + AList[i] * thetaddot[i]

    F = [np.zeros(6) for _ in range(n)]
    tau = np.zeros(n)
    Fplus = np.zeros(6)
    for i in reversed(range(n)):

        Flink = (
            GList[i] @ Vd[i+1]
            - ad(V[i+1]).T @ (GList[i] @ V[i+1])
        )
        F[i] = Flink + Fplus

        tau[i] = F[i] @ AList[i]

        if i != 0:

            Fplus = AdTi[i].T @ F[i]

    return tau


def calculate_dynamics(waypoints, dt, SList, MList, GList, g):
    print("Calculating Dynamic Torques (Tau)...")
    
    theta_array_deg = np.array(waypoints)
    theta_array_rad = np.deg2rad(theta_array_deg) 
    
    thetadot_array = np.gradient(theta_array_rad, dt, axis=0)
    thetaddot_array = np.gradient(thetadot_array, dt, axis=0)

    tau_list = []

    for i in range(len(theta_array_rad)):
        theta = theta_array_rad[i][:3]      
        thetadot = thetadot_array[i][:3]
        thetaddot = thetaddot_array[i][:3]
        
        tau = recursive_newton_euler_algorithm(SList, MList, GList, theta, thetadot, thetaddot, g)
        tau_list.append(tau)

    return np.array(tau_list)


def plot_torque_graph(tau_list, dt):
    time_axis = np.arange(len(tau_list)) * dt
    
    plt.figure(figsize=(10, 6))
    plt.plot(time_axis, tau_list[:, 0], label='Motor 1 (Base) Torque', linewidth=2)
    plt.plot(time_axis, tau_list[:, 1], label='Motor 2 (Shoulder) Torque', linewidth=2)
    plt.plot(time_axis, tau_list[:, 2], label='Motor 3 (Elbow) Torque', linewidth=2)
    
    plt.title("Joint Torques Along the Trajectory (Dynamics)")
    plt.xlabel("Time (Seconds)")
    plt.ylabel("Torque (Nm)")
    plt.legend()
    plt.grid(True)
    plt.show()