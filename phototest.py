import photoresistor

detect = photoresistor.light(0x48)

print(detect.read(2))