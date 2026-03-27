from arduino_serial import motora_aci_gonder
from angle_transforms import angles_motor_transform

def motor_constraints(q0,q1,q2,q3):
    if(q0 < 0 and q0 > 90):
        print("motor0'ın açısı 0 ile 90 derece arası olmalı.")
        return False
    if(q1 < 20 and q1 > 90):
        print("motor1'in açısı 20 ile 90 derece arası olmalı.")
        return False
    if(q2 < 0 and q2 > 80):
        print("motor2'in açısı 0 ile 80 derece arası olmalı.")
        return False
    if(q3 < 20 and q3 > 130):
        print("motor3'in açısı 15 ile 130 derece arası olmalı.")
        return False
    return True


def send_motor_angles(angles,arduino):
    verify = motor_constraints(angles[0],angles[1],angles[2],angles[3])
    if(verify):
        motora_aci_gonder(angles_motor_transform(angles), arduino)
    else:
        print("istenilen acılar calısma alanı dısında")

