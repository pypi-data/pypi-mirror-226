#from DobotEDU import *
import numpy as np
import matplotlib.pyplot as plt


#create line chart 

ret=1

def RotaryTable(rpm = 5,dir=False):
    #magician.set_multiplexing(io="DO_14", multiplex=1)
    #magician.set_multiplexing(io="DO_15", multiplex=1)
    x = (rpm-0.352)/0.003
    #magician.set_do(io="DO_15", level=dir)
    #magician.set_pwm(io="DO_14", freq=x, cycle=50)
    return f"Frecuencia {x}"
def RotaryTablePosition(rpm = 5,dir=False,pos=4):
    #magician.set_infrared_sensor(port=3, enable=True, version=2)
    #magician.set_multiplexing(io="DO_14", multiplex=1)
    #magician.set_multiplexing(io="DO_15", multiplex=1)
    cont=0
    x = (rpm-0.352)/0.003
    #magician.set_do(io="DO_15", level=dir)
    #magician.set_pwm(io="DO_14", freq=x, cycle=50)
    while (cont<pos):
        #vs = magician.get_infrared_sensor(port=3)['status']
        #if vs==1 and va==0:
        cont=cont+1
        #va=vs
    return f"posiciones {cont}"
    #magician.set_pwm(io="DO_14", freq=x, cycle=50)