import RPi.GPIO as GPIO
import time

echo = 22
trig = 27

GPIO.setup(trig,GPIO.OUT)
GPIO.setup