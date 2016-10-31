#encoding:utf-8
#!/usr/bin/env python 
"""
    控制270度舵机，控制线连GPIO_14
"""



import RPi.GPIO as GPIO
import time


class EngineControler(object):

    def __init__(self, pin_num, work_frequency=50):

        self.pin_num = pin_num
        self.pwm = None
        self.__config_pwm(work_frequency)
        self.rote(0)

    def __config_pwm(self, work_frequency=50):

        # set GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_num, GPIO.OUT, initial=False)

        # set PWM
        self.pwm = GPIO.PWM(self.pin_num, work_frequency)
        self.pwm.start(0)

    def rote(self, angle):
        """
        控制旋转角度  0=< angle < =270
        """

        self.pwm.ChangeDutyCycle(2.5 + 10 * angle / 270)
        time.sleep(0.02)
        self.pwm.ChangeDutyCycle(0)
        time.sleep(2)

    def stop(self):

        self.pwm.stop()



if __name__ == "__main__":
    print "start!"
    steer_engine = EngineControler(14)
    for rote in range(0, 271, 30):
        print rote
        steer_engine.rote(rote)
    print "end"





