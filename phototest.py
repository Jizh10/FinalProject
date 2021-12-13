import photoresistor

detect = photoresistor.light(0x48)
while True:
  print(detect.read(1))