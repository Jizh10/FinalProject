from picamera import PiCamera
import json
import time

camera = PiCamera()

try:
  while True:
    with open("/usr/lib/cgi-bin/final_project.txt",'r+') as f:
      data = json.load(f)
      print('data loaded')
      if data['takeImage'] == '1':
        print('command received')
        camera.capture('/www/var/html/image.jpg')
        print('image taken')
        data['takeImage'] == None
        json.dump(data,f)
      time.sleep(0.1)
except KeyboardInterrupt:
  print('\nExiting')

        

        