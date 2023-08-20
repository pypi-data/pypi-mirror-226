from DobotEDU import *
magician.set_multiplexing(io="DO_14", multiplex=1)
magician.set_multiplexing(io="DO_15", multiplex=1)
def RotaryTable(vel, dir):
    x = (vel-0.352)/0.003
    magician.set_do(io="DO_15", level=dir)
    magician.set_pwm(io="DO_14", freq=x, cycle=50)
    return f"Frecuencia {x}"
