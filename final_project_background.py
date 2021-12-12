from picamera import PiCamera
import json
import time

camera = PiCamera()

try:
  while True:
    with open("/usr/lib/cgi-bin/final_project.txt",'r+') as f:
      data = json.load(f)
      if data['take image'] == '1':
        camera.capture('/www/var/html/image.jpg')
        data['take image'] == None
        json.dump(data,f)
      time.sleep(0.1)
except KeyboardInterrupt:
  print('\nExiting')

        

        