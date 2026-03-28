import numpy as np
import time
from angle_transforms import angles_motor_transform

def cubic_trajectory(q0, qf, T, steps=100):
    t = np.linspace(0,T,steps)

    a0 = q0
    a1 = 0
    a2 = 3*(qf - q0)/T**2
    a3 = -2*(qf-q0)/T**3

    q = a0 + a1*t + a2*t**2 + a3*t**3
    return t,q


def generate_trapezoidal_trajectory(start_q, target_q, total_time, dt=0.05):

    step_count = int(total_time / dt)
    tb = total_time / 3.0 
    
    waypoints = []
    
    for i in range(step_count + 1):
        t = i * dt
        instant_angles = []
        
        for j in range(len(start_q)):
            q0 = start_q[j]
            q1 = target_q[j]
            
            if q0 == q1:
                instant_angles.append(q0)
                continue
            
            acceleration = (q1 - q0) / (tb * (total_time - tb))
            
            if t <= tb:
                q_t = q0 + 0.5 * acceleration * (t ** 2)
            elif t <= (total_time - tb):
                q_t = q0 + acceleration * tb * (t - (tb / 2))
            else:
                q_t = q1 - 0.5 * acceleration * ((total_time - t) ** 2)
            
            instant_angles.append(q_t)
            
        waypoints.append(instant_angles)
        
    return waypoints


def yorungeyi_oynat(arduino_baglantisi, yol_noktalari, dt=0.05):
    print("Yörünge başlatılıyor...")

    for anlik_q in yol_noktalari:
        motor_komutlari = angles_motor_transform(anlik_q)
        
        for veri in motor_komutlari:
            mesaj = f"{veri['motor_no']},{veri['aci']}\n"
            arduino_baglantisi.write(mesaj.encode('utf-8'))
        
        arduino_baglantisi.reset_input_buffer()
        time.sleep(dt)
        
    print("Yörünge tamamlandı! Robot hedefe ulaştı.")


def execute_trajectory_and_log(arduino_connection, waypoints, tau_list, dt=0.05):
    print("Trajectory starting...")

    for i, current_q in enumerate(waypoints):
        motor_commands = angles_motor_transform(current_q)
        
        for data in motor_commands:
            message = f"{data['motor_no']},{data['aci']}\n"
            arduino_connection.write(message.encode('utf-8'))
        
        arduino_connection.reset_input_buffer()
        
        current_tau = tau_list[i]
        print(f"Step {i:03d} | Tau (Nm): M1={current_tau[0]:.2f}, M2={current_tau[1]:.2f}, M3={current_tau[2]:.2f}")
        
        time.sleep(dt)
        
    print("Trajectory completed! Robot reached the target.")