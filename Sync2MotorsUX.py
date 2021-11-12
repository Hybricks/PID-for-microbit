# Please look at the version without UX first for more comments

from microbit import *
import machine
import time
import PIDClass

min_PWM = 1100 # min position throttle
max_PWM = 1900 # max throttle

POT_IN = pin2
ESC_MST = pin0
ESC_SLV = pin1

POT_IN.read_analog()

def scale(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def show_PID(K_index):
    for x in range(3):
        for y in range(5):
            if K_index[x] < y:
                display.set_pixel(x*2, -y+4, 0)
            else:
                display.set_pixel(x*2, -y+4, 7)

# A long press on button_a enters into PID adjustment mode
def long_press(button):
    press_t = time.ticks_ms()
    while button.is_pressed():
        if time.ticks_diff(time.ticks_ms(), press_t) > 600:
            while button.is_pressed():
                display.show(Image.YES)   #Confirm a long press
            display.clear()
            return True
    return False
    
ESC_MST.set_analog_period(20)
ESC_SLV.set_analog_period(20)

#getting the ESC's armed
display.show("A")
while not button_a.is_pressed():
    ESC_MST.write_analog(min_PWM/20000 * 1024)
    ESC_SLV.write_analog(min_PWM/20000 * 1024)
    sleep(100)
display.clear()

Kp = [1.0, 1.1, 1.2, 1.3, 1.4]
Ki = [1.0, 1.1, 1.2, 1.3, 1.4]
Kd = [0.000, 0.001, 0.002, 0.003, 0.004, 0.005]

K_index = [2, 0, 1]

PID_SLV = PIDClass.PID(Kp[K_index[0]], Ki[K_index[1]], Kd[K_index[2]] )
PID_SLV.setSampleTime(0.01)  # in s
PID_SLV.setPoint = 0

blink_rate = 200
col = 0
show_PID(K_index)

while True:

    THR_MST = POT_IN.read_analog()
    THR_MST= int(scale(THR_MST, 0, 1024, min_PWM, max_PWM))
    ESC_MST.write_analog(THR_MST/20000 * 1024)

    x = accelerometer.get_x()
    PID_SLV.update(x)
    P_OUT = scale(PID_SLV.output, 1092, -1092, max_PWM, min_PWM) 
    P_OUT = max(min_PWM, min(P_OUT, max_PWM))
    ESC_SLV.write_analog(P_OUT/20000 * 1024)
  
    #Entering adjustment mode
    if long_press(button_a):
        
        ESC_MST.write_analog(min_PWM/20000 * 1024)
        ESC_SLV.write_analog(min_PWM/20000 * 1024)
 
        LED_on = True
        blink_t = time.ticks_ms()
        
        while not long_press(button_a):
            
            if button_a.was_pressed():
                col = (col + 1) % 3
            if button_b.was_pressed():
                K_index[col] = (K_index[col] + 1) % 5
                show_PID(K_index)
            
            K_blink = K_index.copy()
            K_blink[col] = -1
            delta_t = time.ticks_diff(time.ticks_ms(), blink_t)
            
            if delta_t > blink_rate:
                if LED_on:
                    LED_on = False
                    show_PID(K_blink)
                else:
                    LED_on = True
                    show_PID(K_index)
                blink_t = time.ticks_ms()
                
        show_PID(K_index)
        
        PID_SLV.setKp( Kp[K_index[0]] )
        PID_SLV.setKi( Ki[K_index[1]] )
        PID_SLV.setKd( Kd[K_index[2]] )
