import rotational
import numpy as np

stepper = rotational.rot(step = 19, dir = 26)

while True:
  stepper.angle(int(input()))
