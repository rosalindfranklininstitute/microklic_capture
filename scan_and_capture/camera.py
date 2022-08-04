from time import sleep
from picamera import PiCamera
import matplotlib.pyplot as plt
import os
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


def Camera(Picamera):
    @classmethod

    def snapshot(cls):
        # turn on illumination
        ledring= LEDRing()
        ledring.turn_on()

        # set up camera to take
        camera.resolution = 720, 480
        try:
            camera.capture('preview.png')
            img = cv2.imread('preview.png')
            im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print("Camera failed to capture: e")

        # set up figure to display to screen
        if im_rgb:
            plt.figure(1)
            plt.imshow(im_rgb)
            sleep(10)

        #Close plot, delete tmp file and turn off illumination
        plt.close()
        if os.path.isfile('preview.png'):
            try:
                os.remove('preview.png')
            except Exception as e:
                print(e)
                print("Temp file preview.png cannot be removed")
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



    def preview():
        pass

    def stop_and_flush():
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
        camera.close_and_flush()