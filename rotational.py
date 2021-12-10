import RPi.GPIO as GPIO
import time

#step = 19, dir = 26

class rot():

  def __init__(self, step, dir):
    self.step, self.dir = step, dir
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.step, GPIO.OUT, initial=0)
    GPIO.setup(self.dir, GPIO.OUT, initial=0)

  def home(self, val = 0):
    self.cur_angle = val

  def angle(self, angle, speed = 5): #speed in rot/sec
    steps = abs(angle - self.cur_angle)/200
    for i in range(steps):
            GPIO.output(19,1)
            time.sleep(1/(speed*200))
            GPIO.output(19,0)
            time.sleep(1/(speed*200))