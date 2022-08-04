from time import sleep
from picamera import PiCamera
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import board
import neopixel
import sys

class LEDRing:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D18, 20)

    def turn_on(self):
        self.pixels.fill((255, 255, 255))

    def turn_off(self):
        self.pixels.fill((0, 0, 0))

    def turn_on_rgb(r, g, b, self):
        self.pixels.fill((r, g, b))


def Camera(Picamera):
    @classmethod
    def take_photo(cls, save=False, fpath="."):
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


    def preview():
        pass

    def stop_and_flush():
        pass


if __name__=='__main__':
    camera = Camera()
    if sys.argv[1] == 'take_photo':
        camera.take_photo()
    if sys.argv[1] == 'preview':
        camera.preview()

    if sys.argv[1] == 'off':
        camera.close_and_flush()