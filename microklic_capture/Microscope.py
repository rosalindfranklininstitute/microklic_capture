#Microscope
import sys, os
import board
import neopixel
from picamera import PiCamera
from time import sleep
import csv
import numpy as np

#camera = PiCamera()

#camera.resolution = 1920, 1080
#camera.start_preview()
#sleep(10)
#camera.stop_preview()
#del(camera)
#sleep(1)

camera = PiCamera()
camera.resolution = 4056, 3040    
pixels = neopixel.NeoPixel(board.D18, 20)
imagefiletemplate = 'Images/IM{:06d}_R{}_G{}_B{}_EXP{:2f}_ISO{}.png'
filename = 'Input_Array.csv'
row_val = 0

#camera.start_preview()
with open(filename, newline='') as csvfile:
    arrayreader = csv.reader(csvfile, delimiter=' ', quotechar='"')
    for row in arrayreader:
        if row_val == 0:
            lables = ', '.join(row)
            row_val = 1
        else:
            split_str = row[0].split(",")
            imnum = int(split_str[0])
            R = int(split_str[1])
            G = int(split_str[2])
            B = int(split_str[3])
            Exposure = int(split_str[4])
            iso = int(split_str[5])
            camera.shutter_speed = Exposure
            camera.iso = iso
            # set the camera exposure ( means 2^-4 = 1/16 ms)
            #pixels[0] = (R,G,B)
            pixels.fill((R,G,B))
            camera.capture(imagefiletemplate.format(imnum,R,G,B,Exposure,iso))
            print('Saving image'+imagefiletemplate.format(imnum,R,G,B,Exposure,iso))
#camera.stop_preview()



            


