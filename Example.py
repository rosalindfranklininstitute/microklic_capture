#MicroscopeControl
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
from CPcontroller import controller
import os
import cv2
import board
import neopixel
plt.ion()
import subprocess

imagefiletemplate = 'Images{:03d}/IM{:06d}_R{}_G{}_B{}_ISO{}_EXP{}.jpg'


def capture(output_filename, ISO=100, ss=1000000, width=4056, height=3040):
    print('capturing')
    subprocess.Popen(['/usr/bin/raspistill','-w', str(width),'-h', str(height),'-q','100','-n','--awb','off','-cfx','(128:128)','-ISO',str(ISO),'-ss',str(ss),'-o',output_filename]).communicate()
    print('done capturing')


def snap(ISO=50, ss=100000, width=720, height=480):
    plt.figure(1)
    subprocess.Popen(['/usr/bin/raspistill','-w', str(width),'-h', str(height),'-q','100','-n','-ISO',str(ISO),'-ss',str(ss),'-o','snap.jpg']).communicate()
    img = cv2.imread('snap.jpg')
    im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(im_rgb)

pixels = neopixel.NeoPixel(board.D18, 20)
R,G,B, iso, exposure = 255,255,255,100,1
pixels.fill((R,G,B))
# ~ import imutils

#----------------------------------------------------------------------#
#                        Setup file writing
#----------------------------------------------------------------------#
scannumber = 1
filename = "{:06d}.csv".format(scannumber)
imagetemplate = 'Images{:03d}/IM{:06d}.png'
preview_folder = 'Preview'

if os.path.isdir(preview_folder) is not True:
    os.mkdir(preview_folder)
f= open(filename,'a')


#----------------------------------------------------------------------#
#                        Setup Control
#----------------------------------------------------------------------#

cp = controller.cp_control('/dev/ttyUSB0',115200)
cp.connect()
sleep(1)
lp = controller.panel_control('/dev/ttyUSB1',9600)
lp.connect()
sleep(1)
lp.pv(255)
cp.home()
#cp.pos(28.9, 30.8, 45.8)


#----------------------------------------------------------------------#
#                        Setup Camera
#----------------------------------------------------------------------#

#cap = cv2.VideoCapture(2,cv2.CAP_V4L2)
#cap.set(cv2.CAP_PROP_EXPOSURE,-1)


#----------------------------------------------------------------------#
#                        Example Grid Scan
#----------------------------------------------------------------------#

def rgrid(dx,numx,dy,numy,dz,numz,iso,exposure):
    if os.path.isdir('Images{:03d}'.format(scannumber)) is not True:
        os.mkdir('Images{:03d}'.format(scannumber))
    imnum = 1
    f= open(filename,'a')
    f.write('X, Y, Z, image_num\n')
    current_position = cp.getPosition()
    if dx*numx == 0:
        x = [current_position[0]]
    else:
        x = list(np.arange(current_position[0]-(dx*int(numx/2)),current_position[0]+(dx*int(numx/2))+dx,dx))
    if dy*numy == 0:
        y = [current_position[1]]
    else:
        y = list(np.arange(current_position[1]-(dy*int(numy/2)),current_position[1]+(dy*int(numy/2))+dy,dy))
    if dz*numz == 0:
        z = [current_position[2]]
    else:
        z = list(np.arange(current_position[2]-(dz*int(numz/2)),current_position[2]+(dz*int(numz/2))+dz,dz))
    for zval in z:
        for yval in y:
            for xval in x: 
                cp.pos(xval,yval,zval)
                print('exposing')
                capture(imagefiletemplate.format(scannumber,imnum,R,G,B,iso,exposure),iso,exposure*1.e6)
                f.write(str(xval)+','+str(yval)+','+str(zval)+','+'{:05d}'.format(imnum)+'\n')             
                imnum+=1
            x.reverse()
    cp.pos(current_position[0],current_position[1],current_position[2])
    f.close()


lp.pv(255)
# ~ cp.pos(120.51, 95.4, 45.8)
cp.pos(93.2,102,68.8)
snap()


#rgrid(4.2,3,4.2,3,0,0,50,0.1)

