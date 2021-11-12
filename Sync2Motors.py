from microbit import *
import machine
import time
import PIDClass

min_PWM = 1100 # min position throttle. Equals a PWM pulse of 1.1ms
max_PWM = 1900 # max throttle

POT_IN = pin2     # potmeter input
ESC_MST = pin0    # PWM pulse signal for master motor
ESC_SLV = pin1    # PWM pulse signal for slave motor

POT_IN.read_analog()

def scale(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def show_PID(K_index):  # display the PID settings
    for x in range(3):
        for y in range(5):
            if K_index[x] < y:
                display.set_pixel(x*2, -y+4, 0)
            else:
                display.set_pixel(x*2, -y+4, 7)

#Setting the PWM pulse period
ESC_MST.set_analog_period(20)
ESC_SLV.set_analog_period(20)

#Getting the ESC's armed
display.show("A")
while not button_a.is_pressed():
    ESC_MST.write_analog(min_PWM/20000 * 1024)
    ESC_SLV.write_analog(min_PWM/20000 * 1024)
    sleep(100)
display.clear()

Kp = [1.0, 1.1, 1.2, 1.3, 1.4]
Ki = [1.0, 1.1, 1.2, 1.3, 1.4]
Kd = [0.000, 0.001, 0.002, 0.003, 0.004, 0.005]

K_index = [2, 0, 1]   # P=1.2 I=1.0 D=0.001 
show_PID(K_index)

PID_SLV = PIDClass.PID(Kp[K_index[0]], Ki[K_index[1]], Kd[K_index[2]] )
PID_SLV.setSampleTime(0.01)  # in s
PID_SLV.setPoint = 0    # We aim for the vertical position of the Microbit -> motors in sync!


while True:

    THR_MST = POT_IN.read_analog()                 # Read the pot meter
    THR_MST= int(scale(THR_MST, 0, 1024, min_PWM, max_PWM)). # Scale to PWM values
    ESC_MST.write_analog(THR_MST/20000 * 1024)    # Determine the speed of Master motor with potmeter

    x = accelerometer.get_x()                     # Read the angle
    PID_SLV.update(x)                             # Update the PID object
    P_OUT = scale(PID_SLV.output, 1092, -1092, max_PWM, min_PWM) # Scale to PWM values
    P_OUT = max(min_PWM, min(P_OUT, max_PWM))     # Prevent exceeding PWM boundaries
    ESC_SLV.write_analog(P_OUT/20000 * 1024)      # Drive the Slave motor with the outcome of the PID controller
