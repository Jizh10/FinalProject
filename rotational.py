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

  def angle(self, angle, speed = 5*16): #speed in rot/sec
    
    #calculate steps from angle in radians
    steps = (22.918/12.22)*200*16*abs(angle - self.cur_angle)/(2*np.pi)
    #(25.25/13.4) term is gear reduction
    #print("steps {:f}".format(max(int(steps),int(self.partialsteps))))
    #print("steps {:f}".format(steps))
    #if the angle is positive, go one way, negitive go the other
    if angle - self.cur_angle < 0:
      GPIO.output(self.dir,0)
    else:
      GPIO.output(self.dir,1)

    #reset current angle. steps is only is given by the desired angle minus the current angle
    self.cur_angle = angle
    
    #a neat hack
    #the code doesnt work if the angle val is small enough that less than one step is generated, so this code sums all of the unused step bits and holds them until a full step is reached
    if max(int(steps),int(self.partialsteps)) < 8:
      self.partialsteps += steps
    else: self.partialsteps = 0

    if max(int(steps),int(self.partialsteps)) >= 8:
      #on and off on the step input for every step
      for i in range(max(int(steps),int(self.partialsteps))):
        GPIO.output(self.step,1)
        time.sleep(1/(speed*200))
        GPIO.output(self.step,0)
        time.sleep(1/(speed*200))