import Linear.py
import rotational.py
import numpy as np

stepper = rot(step = 19, dir = 26)


class trig():
  def __init__(self):
    pass
  def pointcammera(theta0,d,xc):
      x0 = d*np.cos(theta0)
      y0 = d*np.sin(theta0)

      theta = np.arctan(yi/(xi-xc))
      stepper.move(theta)