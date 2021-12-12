import Linear
import rotational
import numpy as np

stepper = rotational.rot(step = 19, dir = 26)
lin = Linear.Linear()

class trig():
  def __init__(self):
    pass
  def pointcammera(self,theta0,d,xc):
      x0 = d*np.sin(theta0)
      y0 = d*np.cos(theta0)

      theta = np.arctan(y0/(x0-xc))
      print(y0/(x0-xc))
      #stepper.angle(theta)
      
      lin.move(xc)