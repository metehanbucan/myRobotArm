import numpy as np
from fk import FkinSpace
from arduino_serial import motora_aci_gonder
import serial
import time
from angle_transforms import *
from motor_send import *


L1 = 0.094
L2 = 0.135
L3 = 0.147

xdistance = 0.0693

arduino = serial.Serial('COM11', 9600, timeout=1)
time.sleep(2)

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


send_motor_angles(angles,arduino)
arduino.close()
