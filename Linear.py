import odrive
import time
import numpy as np

class Linear():

  def __init__(self):
      self.pulley_diameter = 12.5 #mm
      self.dvr = odrive.find_any()
      #self.dvr.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
      
      #while self.dvr.axis1.current_state != AXIS_STATE_IDLE:
      #  time.sleep(0.1)

      #self.dvr.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

      
  def move(self, pos, speed = 40): #pos in mm, #speed in rot/s
    self.dvr.axis1.controller.config.vel_limit = speed
    self.dvr.axis1.controller.input_pos = pos/(np.PI*self.pulley_diameter)
  
  def home(self):
    #you dont need to call this now, itll do it on boot
    self.dvr.axis1.requested_state = AXIS_STATE_HOMING