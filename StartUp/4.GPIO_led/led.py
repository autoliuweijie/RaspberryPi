# encoding:utf-8
"""
    点亮LED
    电路接法： P20 - 电阻R - 负led正 - Vcc
"""
import RPi.GPIO as GPIO
import time

# config
GPIO.setmode(GPIO.BCM)
led_pin_num = 20
GPIO.setup(led_pin_num, GPIO.OUT, initial=GPIO.HIGH)


# light up led
print "LED light!"
GPIO.output(led_pin_num, 0)
time.sleep(10)
GPIO.output(led_pin_num, 1)
print "LED shutdown!"

GPIO.cleanup()
