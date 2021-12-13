from picamera import PiCamera
from Linear import Linear
from rotational import rot
from distance import ultrasonic
import json
import time
import numpy as np

camera = PiCamera()
camera.rotation = 180
linearMotion = Linear()
rotation = rot(19,26)
ultrasonic = ultrasonic(22,27)
imageIndex = 1

try:
  while True:
    with open("/usr/lib/cgi-bin/final_project.txt",'r+') as f:
      data = json.load(f)

      linearMotion.move(20*int(data['displayPos']))
      rotation.angle(float(data['displayAngle'])/180.0*np.pi)
      if data['detect'] == 'y':
        distance = ultrasonic.getDist()
        data['detect'] = str(int(distance))
      # print('data loaded')
      if data['takeImage'] == '1':
      #   print('command received')
        camera.capture('/var/www/html/%s.jpg' % imageIndex, use_video_port=True)
        #print('image taken')
        data['takeImage'] = None
      f.seek(0)
      json.dump(data,f)
      time.sleep(0.1)
except KeyboardInterrupt:
  print('\nExiting')

        

        