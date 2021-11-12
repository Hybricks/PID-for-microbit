# Aangepaste PID controller - werkt! 

# Ivmech PID Controller is simple implementation of a
# Proportional-Integral-Derivative (PID) Controller in the Python Programming Language.
# More information about PID Controller: http://en.wikipedia.org/wiki/PID_controller

import time


class PID:
    def __init__(self, P=0.2, I=0.0, D=0.0):

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = 0
        self.current_time = time.ticks_ms()
        self.last_time = self.current_time

        self.clear()

    def clear(self):
        # Clears PID computations and coefficients
        self.SetPoint = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        self.output = 0.0

    def update(self, feedback_value):
        # u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}
        # Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)

        error = self.SetPoint - feedback_value

        self.current_time = time.ticks_ms()

        delta_time = time.ticks_diff(self.current_time, self.last_time) / 1000
        delta_error = error - self.last_error

        if delta_time >= self.sample_time:
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)


    def setKp(self, proportional_gain):
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        self.Kd = derivative_gain

    def setSampleTime(self, sample_time):
        # PID that should be updated at a regular interval.
        # Based on a pre-determined sample time, the PID decides
        # if it should compute or return immediately.
        self.sample_time = sample_time
