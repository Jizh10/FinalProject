from picamera import PiCamera
from Linear import Linear
import json
import time

camera = PiCamera()
linearMotion = Linear()

try:
  while True:
    with open("/usr/lib/cgi-bin/final_project.txt",'r+') as f:
      data = json.load(f)

      linearMotion.move(data[''])
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

        

        