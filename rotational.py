import RPi.GPIO as GPIO
import time
import numpy as np
#step = 19, dir = 26

class rot():

  def __init__(self, step, dir):
    self.step, self.dir = step, dir
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.step, GPIO.OUT, initial=0)
    GPIO.setup(self.dir, GPIO.OUT, initial=0)
    self.cur_angle = 0

  def home(self, val = 0):
    self.cur_angle = val

  def angle(self, angle, speed = 5): #speed in rot/sec
    steps = abs(angle - self.cur_angle)/(200*2*np.pi)
    print(steps)
    if angle - self.cur_angle < 0:
      GPIO.output(self.dir,0)
    else:
      GPIO.output(self.dir,1)
    for i in range(1000):#int(steps)):
            GPIO.output(self.step,1)
            time.sleep(1/(speed*200))
            GPIO.output(self.step,0)
            time.sleep(1/(speed*200))