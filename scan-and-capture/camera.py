from time import sleep
from picamera import PiCamera
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import board
import neopixel
import sys
import argparse

class LEDRing:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D18, 20)

    def turn_on(self):
        self.pixels.fill((255, 255, 255))

    def turn_off(self):
        self.pixels.fill((0, 0, 0))

    def turn_on_rgb(r, g, b, self):
        self.pixels.fill((r, g, b))


class Camera(Picamera):
    @classmethod

    def snapshot(cls):
        # turn on illumination
        ledring= LEDRing()
        ledring.turn_on()

        # set up camera to take
        camera.resolution = 720, 480
        camera.capture('preview.png')
        img = cv2.imread('preview.png')
        im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # set up figure to display to screen
        plt.figure(1)
        plt.imshow(im_rgb)
        sleep(10)

        #Close plot, delete tmp file and turn off illumination
        plt.close()
        if os.path.isfile('preview.png'):
            os.remove('preview.png')
        ledring.turn_off()

    @classmethod
    def take_photo(cls, save=True, fpath='preview.png'):
        # turn on illumination
        ledring = LEDRing()
        ledring.turn_on()

        # set up camera to take
        camera.resolution = 720, 480
        camera.capture(fpath)
        img = cv2.imread(fpath)
        im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # set up figure to display to screen
        plt.figure(1)
        plt.imshow(im_rgb)
        sleep(10)
        # Close plot, delete tmp file and turn off illumination
        plt.close()


    @classmethod
    def rfi_preview(cls):
       
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
    
        camera = PiCamera()
        camera.rotation =180

        frame = 1
        while True:
            try:
                camera.start_preview(alpha=150)
         
            except KeyboardInterrupt:
                camera.stop_preview()
                camera.close()
                break

    def close_and_flush():
       # https://forums.raspberrypi.com/viewtopic.php?t=152239
        camera = PiCamera()
        camera.stop_preview() #review later
     )
        pass

if __name__=='__main__':
    camera = Camera()
    if sys.argv[1] == 'snapshot':
        camera.take_photo()

    if sys.argv[1] == 'take_photo':
        parser = argparse.ArgumentParser()
        parser.add_argument(dest='save', type="bool", help="This is the first argument")
        parser.add_argument(dest='fpath', type="str", help="This is the first argument")
        args = parser.parse_args()
        camera.take_photo(args.save, args.fpath)

    if sys.argv[1] == 'preview':
        camera.preview()

    if sys.argv[1] == 'off':
        print('try ctrl-D to stop the script, ')
        camera.close_and_flush()