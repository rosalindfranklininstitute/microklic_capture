#Microscope
import sys, os
import board
import neopixel
from picamera import PiCamera
from time import sleep
import csv
import numpy as np
import os

import subprocess

def capture(output_filename, ISO=100, ss=1000000):
    print('capturing')
    subprocess.Popen(['/usr/bin/raspistill','-q','100','-n','--awb','off','-ISO',str(ISO),'-ss',str(ss),'-cfx','(128:128)','-o',output_filename]).communicate()
    print('done capturing')

def check_and_make_image_folder(image_folder):
    if not os.path.isdir(image_folder):
        os.mkdir(image_folder)
        print("creating new image dir")
    else:
        print("directory, exists rewrite to exisiting dir")
#capture('test55.jpg')
    
def main(image_folder="Images"):

    pixels = neopixel.NeoPixel(board.D18, 20)
    check_and_make_image_folder(image_folder)
    imagefiletemplate = image_folder + '/IM{:06d}.jpg'
    filename = 'Input_Array.csv'
    row_val = 0

    # sorting white balance
    pixels.fill((255,255,255))
    subprocess.Popen(['/usr/bin/raspistill','-t','30000','-awb','auto','-ISO','100','-ss','100000','-cfx','(128:128)']).communicate()


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
                position = split_str[6]
                print("["+position+"]")
                if (position == 'all'):
                    pixels.fill((R,G,B))
                else:
                    pixels.fill((0,0,0))
                    for i in (-1, 0, 1):
                        pixels[int(position)+i] = (R,G,B) 
                capture(imagefiletemplate.format(imnum), ISO=iso, ss=Exposure)
                print('Saving image '+imagefiletemplate.format(imnum))
    pixels.fill(0)
    
import sys
if __name__=="__main__":
    main(sys.argv[1])
