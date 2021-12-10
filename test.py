import trig
import distance
import time
import numpy as np

sens = distance.ultrasonic(echo = 22, trig = 27)
trig = trig.trig()

dists = []
#average
for i in range(10):
  np.append(dists,sens.getDist())
  time.sleep(0.1)

dist = np.average(dists)

