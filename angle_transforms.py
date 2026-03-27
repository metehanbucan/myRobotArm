import numpy as np

def deg_to_rad(angles):
    rads = []
    length = len(angles)
    for i in range (length):
        rads.append(angles[i] * np.pi / 180)
    return rads

def rad_to_deg(rad):
    return rad * 180 / np.pi

def angles_motor_transform(angles):
    q0 = angles[0]
    q1 = angles[1]
    q2 = angles[2] + angles[1]
    q3 = angles[3]
    motor_komutlari = []
    pwm_0 = int(150 + (q0 * 2.5)) 
    motor_komutlari.append({"motor_no": 0, "aci": pwm_0})
    pwm_1 = int(561 - (2.625 * q1))
    motor_komutlari.append({"motor_no": 1, "aci": pwm_1})
    pwm_2 = int(520 + (2 * q2))
    motor_komutlari.append({"motor_no": 2, "aci": pwm_2})
    if q3 > 0:
        pwm_3 = 450 # Kıskaç kapalı PWM (Kendine göre ayarla)
    else:
        pwm_3 = 200 # Kıskaç açık PWM
    motor_komutlari.append({"motor_no": 3, "aci": pwm_3})
    
    return motor_komutlari