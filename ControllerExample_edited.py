#MicroscopeControl
from time import sleep
from picamera import PiCamera
import matplotlib.pyplot as plt
import numpy as np
from CPcontroller import controller
import os
import cv2
import board
import neopixel
plt.ion()
camera = PiCamera()
camera.resolution = 1920, 1080
#camera.resolution = 4056, 3040 

imagefiletemplate = 'Images{:03d}/IM{:06d}_R{}_G{}_B{}_EXP{:2f}_ISO{}.png'



pixels = neopixel.NeoPixel(board.D18, 20)
R,G,B,Exposure,iso = 255,255,255,0.2,1000
pixels.fill((R,G,B))
# ~ import imutils

#----------------------------------------------------------------------#
#                        Setup file writing
#----------------------------------------------------------------------#
scannumber = 2
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

def rgrid(dx,numx,dy,numy,dz,numz,exposure):
    if os.path.isdir('Images{:03d}'.format(scannumber)) is not True:
        os.mkdir('Images{:03d}'.format(scannumber))
    camera.resolution = 1920, 1080
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
                sleep(exposure) # Camera interrogation command here
                print('exposing')
                camera.capture(imagefiletemplate.format(scannumber,imnum,R,G,B,Exposure,iso))
                f.write(str(xval)+','+str(yval)+','+str(zval)+','+'{:05d}'.format(imnum)+'\n')

              
                imnum+=1
            x.reverse()
    cp.pos(current_position[0],current_position[1],current_position[2])
    f.close()

def snap():
    plt.figure(1)
    camera.resolution = 720, 480
    camera.capture('preview.png')
    img = cv2.imread('preview.png')
    im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(im_rgb)

snap()    

lp.pv(255)
# ~ cp.pos(120.51, 95.4, 45.8)
cp.pos(92.2,102.6,68.3)
#rgrid(4.2,3,4.2,3,0,0,1)

#PREVIEW METHOD
def start_preview(self, **options):
        """
        Displays the preview overlay.

        This method starts a camera preview as an overlay on the Pi's primary
        display (HDMI or composite). A :class:`PiRenderer` instance (more
        specifically, a :class:`PiPreviewRenderer`) is constructed with the
        keyword arguments captured in *options*, and is returned from the
        method (this instance is also accessible from the :attr:`preview`
        attribute for as long as the renderer remains active).  By default, the
        renderer will be opaque and fullscreen.

        This means the default preview overrides whatever is currently visible
        on the display. More specifically, the preview does not rely on a
        graphical environment like X-Windows (it can run quite happily from a
        TTY console); it is simply an overlay on the Pi's video output. To stop
        the preview and reveal the display again, call :meth:`stop_preview`.
        The preview can be started and stopped multiple times during the
        lifetime of the :class:`PiCamera` object.

        All other camera properties can be modified "live" while the preview is
        running (e.g. :attr:`brightness`).

        .. note::

            Because the default preview typically obscures the screen, ensure
            you have a means of stopping a preview before starting one. If the
            preview obscures your interactive console you won't be able to
            Alt+Tab back to it as the preview isn't in a window. If you are in
            an interactive Python session, simply pressing Ctrl+D usually
            suffices to terminate the environment, including the camera and its
            associated preview.
        """
        self._check_camera_open()
        self._preview.close()
        options.setdefault('layer', self._preview_layer)
        options.setdefault('alpha', self._preview_alpha)
        options.setdefault('fullscreen', self._preview_fullscreen)
        options.setdefault('window', self._preview_window)
        renderer = PiPreviewRenderer(
            self, self._camera.outputs[self.CAMERA_PREVIEW_PORT], **options)
        self._preview = renderer
        return renderer

#For ctrl+C:
button = Button(17)
camera = PiCamera()
camera.rotation =180

frame = 1

while True:
    try:
        camera.start_preview(alpha=150)
        button.wait_for_press()
        camera.capture('/home/pi/animation/frame%03d.jpg' % frame)
        frame += 1
    except KeyboardInterrupt:
        camera.stop_preview()
        camera.close()
        break