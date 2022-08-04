from time import sleep
from picamera import PiCamera
import matplotlib.pyplot as plt
import numpy as np
from CPcontroller import controller
import os
import cv2
import board
import neopixel
from camera import Camera, LEDRing
import sys


def main(fpath):
    if os.path.isdir(fpath) is not True:
        os.mkdir(fpath)


    stage_move = controller.cp_control('/dev/ttyUSB0', 115200)
    stage_move.connect()

    camera = Camera()
    camera.resolution = 1920, 1080

    ledring = LEDRing()
    ledring.turn_on()



    # Start Scan
    start_position = stage_move.getPosition()

    x = list(np.arange(start_position[0] , start_position[0]+ stp_sz_x * int(num_stps_z ), stp_sz_x))
    y = list(np.arange(start_position[1], start_position[1] + stp_sz_y * int(num_stps_y), stp_sz_y))
    pos_z = start_position[2]


    for pos_x in x :
       for pos_y in y:

           stage_move.pos(pos_x, pos_y, pos_z)
           sleep(1)
           camera.take_photo(save=True, fpath=f'{fpath}/im_x{pos_x}_y{posy}.jpeg')
           sleep(1)

    stage_move.pos(start_position[0],start_position[1],start_position[2])

    ledring.turn_off()


if __name__ == '__main__':
    # sys.argv[1] path name add
    main(sys.argv[1])