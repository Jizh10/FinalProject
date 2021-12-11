import RPi.GPIO as GPIO
import time

#echo = 22, trig = 27

class ultrasonic():

  def __init__(self,echo,trig):
    self.echo = echo
    self.trig = trig
    GPIO.setup(self.trig,GPIO.OUT)
    GPIO.setup(self.echo, GPIO.IN)

  def getDist(self):
    GPIO.output(self.trig, 1)
    time.sleep(0.00001)
    GPIO.output(self.trig, 0)

    while GPIO.input(self.echo) == 0:
      t1 = time.time()

    while GPIO.input(self.echo) == 1:
      t2 = time.time()
    
    t = t2-t1

    dist = (t*343000)/2 #dist in mm

    return dist