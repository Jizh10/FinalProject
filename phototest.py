import photoresistor

detect = photoresistor.light(2)

print(detect.read())