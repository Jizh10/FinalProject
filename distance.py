import RPi.GPIO as GPIO
import time

#echo = 22, trig = 27

class getDist():

  def __init__(self,echo,trig):
    self.echo = echo
    self.trig = trig
    GPIO.setup(self.trig,GPIO.OUT)
    GPIO.setup(self.echo, GPIO.IN)

  