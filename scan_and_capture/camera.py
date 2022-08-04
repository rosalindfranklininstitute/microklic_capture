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
        # illuminate Pixels
        pass

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