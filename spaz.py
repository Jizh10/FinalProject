import time
import numpy as np
import rotational
import Linear
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

stepper = rotational.rot(step = 19, dir = 26)

lin = Linear.Linear()

lin.move(0)


try:
  while True:
    for i in np.append(range(0,900,50),range(900,0,-50)):
      xc = i
      print("xc {:f}".format(xc))
      lin.move(xc)
      time.sleep(.1/1000)
except KeyboardInterrupt:
  stepper.angle(0)
  GPIO.cleanup()

stepper.angle(0)
GPIO.cleanup()