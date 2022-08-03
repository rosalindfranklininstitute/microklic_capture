#MicroscopeControl
from time import sleep
from picamera import PiCamera
import numpy as np
from CPcontroller import controller
import os
import cv2
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 20)
R,G,B, = 255,255,255
pixels.fill((R,G,B))

cp = controller.cp_control('/dev/ttyUSB0',115200)
cp.connect()
sleep(1)
lp = controller.panel_control('/dev/ttyUSB1',9600)
lp.connect()
sleep(1)
lp.pv(255)
cp.home()

print('Commands:')
print('To position microscope: cp.pos(x,y,z)')
print('Incremental move: cp.inc(x,y,z)')
print('To set panel brightness: lp.pv(255)')
print('To set ring light colour and brightness: pixels.fill((R,G,B))')
print('For live streaming of the camera while positioning, open another terminal and paste the command\n  raspistill -t 0 -p 0,0,300,300')



