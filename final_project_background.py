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
        camera.capture('/var/www/html/1.jpg')
        print('image taken')
        data['takeImage'] = None
        f.seek(0)
        json.dump(data,f)
        f.truncate()
      time.sleep(0.1)
except KeyboardInterrupt:
  print('\nExiting')

        

        