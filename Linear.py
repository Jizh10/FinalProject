import odrive
#import time
import numpy as np

class Linear():

  def __init__(self):
      self.pulley_diameter = 12.5 #mm
      self.dvr = odrive.find_any()
      #self.dvr.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
      
      #while self.dvr.axis1.current_state != AXIS_STATE_IDLE:
      #  time.sleep(0.1)

      self.dvr.axis1.requested_state = 8#AXIS_STATE_CLOSED_LOOP_CONTROL
      self.dvr.clear_errors()

      
  def move(self, pos, speed = 40): #pos in mm, #speed in rot/s
    
    #self.dvr.axis1.requested_state = #8#AXIS_STATE_CLOSED_LOOP_CONTROL
    #self.dvr.axis1.controller.config.vel_limit = speed
    self.curr_pos = pos
    self.dvr.axis1.controller.input_pos = -1*pos/(np.pi*self.pulley_diameter)
    
  def home(self):
    #you dont need to call this now, itll do it on boot
    self.dvr.axis1.requested_state = AXIS_STATE_HOMING