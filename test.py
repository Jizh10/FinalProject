import trig
import distance
import time
import numpy as np
import rotational

sens = distance.ultrasonic(echo = 22, trig = 27)
trig = trig.trig()

stepper = rotational.rot(step = 19, dir = 26)

dists = []
#average
for i in range(10):
  dists = np.append(dists,sens.getDist())
  time.sleep(0.1)

dist = np.average(dists)
angle = 0

for i in range(10):
  print(angle,dist,i*10)

  trig.pointcammera(angle, dist, i*10)
  
  time.sleep(5)