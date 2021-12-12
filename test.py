import distance
import time
import numpy as np
import rotational
import Linear
import RPiGPIO as GPIO

sens = distance.ultrasonic(echo = 22, trig = 27)
lin = Linear.Linear()

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
  for i in range(1000):
    xc = i

    theta = np.arctan((x0-xc)/y0)
    print("theta {:f}".format(theta))
    print("xc {:f}".format(xc))
    print("y0 {:f}".format(y0))
    stepper.angle(theta)
    lin.move(xc)
    
    time.sleep(0.01)
except:
  stepper.angle(0)
  GPIO.cleanup()
