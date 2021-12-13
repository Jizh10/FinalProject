import distance
import time
import numpy as np
import rotational
import Linear
import RPi.GPIO as GPIO

sens = distance.ultrasonic(echo = 22, trig = 27)
lin = Linear.Linear()

lin.move(0)

stepper = rotational.rot(step = 19, dir = 26)

dists = []
#average
for i in range(10):
  dists = np.append(dists,sens.getDist())
  time.sleep(0.1)

dist = np.average(dists)

print("dist =")
print(dist)
theta0 = 0.001
x0 = dist*np.sin(theta0)
y0 = dist*np.cos(theta0)
try:
  while True:
    for i in np.append(range(0,900),range(900,0,-1)):
      xc = i
      print(i)
      theta = np.arctan((x0-xc)/y0)
      print("theta {:f}".format(theta))
      print("xc {:f}".format(xc))
      print("y0 {:f}".format(y0))
      stepper.angle(theta)
      lin.move(xc)
      
      time.sleep(0.0005)
except:
  stepper.angle(0)
  GPIO.cleanup()