import numpy as np
from fk import FkinSpace
from ik import analytic_ik
from arduino_serial import motora_aci_gonder
import serial
import time
from angle_transforms import *
from motor_send import *
from trajectory import generate_trapezoidal_trajectory, execute_trajectory_and_log
from dynamic import calculate_dynamics, plot_torque_graph


L1 = 0
L2 = 0.135
L3 = 0.147

xdistance = 0.0693


M = np.array([[1,0,0,L2+L3],
              [0,1,0,0],
              [0,0,1,L1],
              [0,0,0,1]])

S1 = np.array([0,0,1,0,0,0])
S2 = np.array([0,-1,0,L1,0,0])
S3 = np.array([0,-1,0,L1,0,-L2])

SList = np.array([S1,S2,S3]).T


angles = [45,90,-135,0]
fk_angles = [45 - angles[0], angles[1], angles[2], angles[3]]
print(FkinSpace(SList,deg_to_rad(fk_angles),M))
theta1,theta2,theta3 = analytic_ik(0.1039447 + 0.0693 , 0, 0.1250553, L1, L2,L3)
print(theta1, theta2,theta3)
print(FkinSpace(SList,np.array([theta1,theta2,theta3,0]),M))

gravity_g = np.array([0, 0, 9.81])
G1 = np.array([[4.126e-4, -3.565e-6, 6.653e-6,0,0,0],
               [-3.565e-6, 1.945e-4, 5.462e-6,0,0,0],
               [6.653e-6, 5.542e-6, 3.883e-4,0,0,0],
               [0,0,0,0.327,0,0],
               [0,0,0,0,0.327,0],
               [0,0,0,0,0,0.327]])

G2 = np.array([[1.530e-5, -1.032e-6, 1.454e-6,0,0,0],
               [-1.032e-6, 1.917e-4, 4.094e-7,0,0,0],
               [1.454e-6, 4.094e-7, 1.938e-4,0,0,0],
               [0,0,0,0.09,0,0],
               [0,0,0,0,0.09,0],
               [0,0,0,0,0,0.09]])

G3 = np.array([[1.739e-5, 2.298e-5, 4.002e-5,0,0,0],
               [2.298e-5, 0.001, 1.163e-7,0,0,0],
               [4.002e-5, 1.163e-7, 0.001,0,0,0],
               [0,0,0,0.093,0,0],
               [0,0,0,0,0.093,0],
               [0,0,0,0,0,0.093]])

M01 = np.array([[1,0,0,-3.762e-4],
                [0,1,0,0.004],
                [0,0,1,-0.021],
                [0,0,0,1],])

M12 = np.array([[1,0,0,0.058],
                [0,1,0,0.002],
                [0,0,1,-0.05],
                [0,0,0,1],])

M23 = np.array([[1,0,0,0.187],
                [0,1,0,0.009],
                [0,0,1,0.058],
                [0,0,0,1],])
M34 = np.array([[1,0,0,0.137],
                [0,1,0,-0.009],
                [0,0,1,0.058],
                [0,0,0,1],])
GList = np.array([G1,G2,G3])
MList = np.array([M01,M12,M23,M34])


current_angles = [0, 90, -90, 0]
target_angles = [0, 90, -90, 0]
#target_angles = [45, 30, -90, 0]
movement_time = 3.0
time_step = 0.05
waypoints = generate_trapezoidal_trajectory(
        current_angles, 
        target_angles, 
        total_time=movement_time, 
        dt=time_step
    )

calculated_torques = calculate_dynamics(
        waypoints, 
        time_step, 
        SList, 
        MList, 
        GList, 
        gravity_g
    )

plot_torque_graph(calculated_torques, time_step)

user_input = input("\nGrafiği incelediniz. Hareketi fiziksel robota göndermek istiyor musunuz? (Y/N): ")

if user_input.upper() == 'Y':
    print("Bağlantı kuruluyor...")
    arduino = serial.Serial('COM11', 115200, timeout=1)
    time.sleep(2)
    execute_trajectory_and_log(arduino, waypoints, calculated_torques, dt=time_step)
    arduino.close()
    print("İşlem tamamlandı!")
else:
    print("Hareket iptal edildi. Simülasyon sonlandırılıyor.")
