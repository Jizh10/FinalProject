#!/usr/bin/env python

# the base of the code came from https://github.com/waveform80/pistreaming/ we utilized the video streaming code and embedded our control code into it so that we can use the pi camera to simutaneously stream video, take images, and control the movement. The control code is embedded into the main method.
import json
from Linear import Linear
from rotational import rot
from distance import ultrasonic
from photoresistor import light
import RPi.GPIO as GPIO
import numpy as np


import sys
import io
import os
import shutil
from subprocess import Popen, PIPE
from string import Template
from struct import Struct
from threading import Thread
from time import sleep, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from wsgiref.simple_server import make_server

import picamera
from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import (
    WSGIServer,
    WebSocketWSGIHandler,
    WebSocketWSGIRequestHandler,
)
from ws4py.server.wsgiutils import WebSocketWSGIApplication

###########################################
# CONFIGURATION
WIDTH = 640
HEIGHT = 480
FRAMERATE = 24
HTTP_PORT = 8082
WS_PORT = 8084
COLOR = u'#444'
BGCOLOR = u'#333'
JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')
VFLIP = False
HFLIP = False

###########################################


class StreamingHttpHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
            return
        elif self.path == '/jsmpg.js':
            content_type = 'application/javascript'
            content = self.server.jsmpg_content
        elif self.path == '/index.html':
            content_type = 'text/html; charset=utf-8'
            tpl = Template(self.server.index_template)
            content = tpl.safe_substitute(dict(
                WS_PORT=WS_PORT, WIDTH=WIDTH, HEIGHT=HEIGHT, COLOR=COLOR,
                BGCOLOR=BGCOLOR))
        else:
            self.send_error(404, 'File not found')
            return
        content = content.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(content))
        self.send_header('Last-Modified', self.date_time_string(time()))
        self.end_headers()
        if self.command == 'GET':
            self.wfile.write(content)


class StreamingHttpServer(HTTPServer):
    def __init__(self):
        super(StreamingHttpServer, self).__init__(
                ('', HTTP_PORT), StreamingHttpHandler)
        with io.open('index.html', 'r') as f:
            self.index_template = f.read()
        with io.open('jsmpg.js', 'r') as f:
            self.jsmpg_content = f.read()


class StreamingWebSocket(WebSocket):
    def opened(self):
        self.send(JSMPEG_HEADER.pack(JSMPEG_MAGIC, WIDTH, HEIGHT), binary=True)


class BroadcastOutput(object):
    def __init__(self, camera):
        print('Spawning background conversion process')
        self.converter = Popen([
            'ffmpeg',
            '-f', 'rawvideo',
            '-pix_fmt', 'yuv420p',
            '-s', '%dx%d' % camera.resolution,
            '-r', str(float(camera.framerate)),
            '-i', '-',
            '-f', 'mpeg1video',
            '-b', '800k',
            '-r', str(float(camera.framerate)),
            '-'],
            stdin=PIPE, stdout=PIPE, stderr=io.open(os.devnull, 'wb'),
            shell=False, close_fds=True)

    def write(self, b):
        self.converter.stdin.write(b)

    def flush(self):
        print('Waiting for background conversion process to exit')
        self.converter.stdin.close()
        self.converter.wait()


class BroadcastThread(Thread):
    def __init__(self, converter, websocket_server):
        super(BroadcastThread, self).__init__()
        self.converter = converter
        self.websocket_server = websocket_server

    def run(self):
        try:
            while True:
                buf = self.converter.stdout.read1(32768)
                if buf:
                    self.websocket_server.manager.broadcast(buf, binary=True)
                elif self.converter.poll() is not None:
                    break
        finally:
            self.converter.stdout.close()


def main():
    imageIndex = 1
    linearMotion = Linear()
    rotation = rot(19,26)
    distSensor = ultrasonic(22,27)
    photoRes = light(0x48)
    setDist = 0
    setPos = 0
    setAngle = 0
    print('Initializing camera')
    with picamera.PiCamera() as camera:
        camera.rotation = 180
        camera.resolution = (WIDTH, HEIGHT)
        camera.framerate = FRAMERATE
        camera.vflip = VFLIP # flips image rightside up, as needed
        camera.hflip = HFLIP # flips image left-right, as needed
        sleep(1) # camera warm-up time
        print('Initializing websockets server on port %d' % WS_PORT)
        WebSocketWSGIHandler.http_version = '1.1'
        websocket_server = make_server(
            '', WS_PORT,
            server_class=WSGIServer,
            handler_class=WebSocketWSGIRequestHandler,
            app=WebSocketWSGIApplication(handler_cls=StreamingWebSocket))
        websocket_server.initialize_websockets_manager()
        websocket_thread = Thread(target=websocket_server.serve_forever)
        print('Initializing HTTP server on port %d' % HTTP_PORT)
        http_server = StreamingHttpServer()
        http_thread = Thread(target=http_server.serve_forever)
        print('Initializing broadcast thread')
        output = BroadcastOutput(camera)
        broadcast_thread = BroadcastThread(output.converter, websocket_server)
        print('Starting recording')
        camera.start_recording(output, 'yuv')
        try:
            print('Starting websockets thread')
            websocket_thread.start()
            print('Starting HTTP server thread')
            http_thread.start()
            print('Starting broadcast thread')
            broadcast_thread.start()
            ####################################
            # this section is the code that determines the state of the camera
            while True:
              # open the file that has the json data to read and write
              with open("/usr/lib/cgi-bin/final_project.txt",'r+') as f:
                # load the data
                data = json.load(f)
                #print('data loaded')

                # adjust the linear postion
                linearMotion.move(20*int(data['displayPos']))
                # adjust the angular position
                rotation.angle(float(data['displayAngle'])/180.0*np.pi)
                
                # check if the user wants to detect an object
                if data['detect'] == 'detect':
                  # use the ultrasonic sense to get the distance
                  distance = distSensor.getDist()
                  setDist = distance
                  # set the value of key 'detect' to it
                  data['detect'] = str(distance)
                  # go to the beginning of the document
                  f.seek(0)
                  # dump the data
                  json.dump(data,f)

                # check if the user wants to take an image
                if data['takeImage'] == '1':
                  # increase image index
                  imageIndex += 1
                  print('command received')
                  # capture the image
                  camera.capture('/var/www/html/%s.jpg' % imageIndex, use_video_port=True)
                  print('image taken')
                  # reset take image so it only takes one image
                  data['takeImage'] = None
                  # go to the beginning of the document
                  f.seek(0)
                  # dump the data
                  json.dump(data,f)
                
                # check if the user wants to set a position
                if data['posSet'] == 'set position':
                  # set the position
                  setPos = 20*int(data['displayPos'])
                  setAngle = float(data['displayAngle'])/180.0*np.pi
                  print(setPos)
                  print(setAngle)

                # check if the user wants to use the auto mode
                if data['auto'] == 'auto':
                  # reset the auto
                  data['auto'] = "not auto"
                  # go to the beginning of the document
                  f.seek(0)
                  # dump the data
                  json.dump(data,f)

                  # set the x, y position of the object
                  x0 = setPos + setDist*np.sin(setAngle)
                  y0 = setDist*np.cos(setAngle)
                  print('set Position is %f' % setPos)
                  print("x0 is: %f" % x0)
                  print("y0 is: %f" % y0)
                  # go to 0 point
                  linearMotion.move(0)
                  # set the angle to 0
                  rotation.angle(0)

                  # for each position from 0 to 900mm
                  for i in range(0, 900):
                    # set the current position
                    xc = i
                    # calculate the angle
                    theta = np.arctan((x0-xc)/y0)
                    # go to the angle
                    if i % 10 == 0:
                      rotation.angle(theta, speed=20*16*5)

                    sleep(5/1000)
                    # go to the position
                    linearMotion.move(xc)
                    print(theta)
                    
                    # if its an increment of 90mm take an image (total of 10)
                    if i % 90 == 0:
                      imageIndex += 1
                      print("image taken")
                      camera.capture('/var/www/html/%s.jpg' % imageIndex, use_video_port=True)
                    # scale the brightness based on the photoresistor reading
                    brightness = photoRes.read(0)
                    camera.brightness = int(brightness)  

                  # go back to the original position and angle
                  print(setAngle)
                  linearMotion.move(setPos)
                  rotation.angle(setAngle)
                  
                # adjust the brightness based on the photoresistor reading
                brightness = photoRes.read(0)
                camera.brightness = int(brightness)
                camera.wait_recording(1)
        except KeyboardInterrupt:
            pass
        finally:
            print('Stopping recording')
            camera.stop_recording()
            print('Waiting for broadcast thread to finish')
            broadcast_thread.join()
            print('Shutting down HTTP server')
            http_server.shutdown()
            print('Shutting down websockets server')
            websocket_server.shutdown()
            print('Waiting for HTTP server thread to finish')
            http_thread.join()
            print('Waiting for websockets thread to finish')
            websocket_thread.join()
            GPIO.cleanup()



if __name__ == '__main__':
    main()