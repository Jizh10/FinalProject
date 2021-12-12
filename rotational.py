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
    self.partialsteps = 0

  def home(self, val = 0):
    self.cur_angle = val

  def angle(self, angle, speed = 5): #speed in rot/sec
    steps = (25.25/13.4)*200*abs(angle - self.cur_angle)/(2*np.pi)
    #(25.25/13.4) term is gear reduction
    print("steps {:f}".format(max(int(steps),int(self.partialsteps))))
    
    if angle - self.cur_angle < 0:
      GPIO.output(self.dir,0)
    else:
      GPIO.output(self.dir,1)
    self.cur_angle = angle
    
    if steps < 1:
      self.partialsteps += steps
    else: self.partialsteps = 0

    for i in range(max(int(steps),int(self.partialsteps))):
            GPIO.output(self.step,1)
            time.sleep(1/(speed*200))
            GPIO.output(self.step,0)
            time.sleep(1/(speed*200))