from picamera import PiCamera
from Linear import Linear
from rotational import rot
import json
import time
import numpy as np

camera = PiCamera()
linearMotion = Linear()
rotation = rot(19,26)

try:
  while True:
    with open("/usr/lib/cgi-bin/final_project.txt",'r+') as f:
      data = json.load(f)

      linearMotion.move(20*int(data['displayPos']))
      rotation.angle(float(data['displayAngle'])/180.0*np.pi)
      # print('data loaded')
      # if data['takeImage'] == '1':
      #   print('command received')
      #   camera.capture('/var/www/html/image.jpg')
      #   print('image taken')
      #   data['takeImage'] = None
      #   f.seek(0)
      #   json.dump(data,f)
      time.sleep(0.1)
except KeyboardInterrupt:
  print('\nExiting')

        

        