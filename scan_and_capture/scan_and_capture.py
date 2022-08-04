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

def main():

    ledring= LEDRing
    ledring.turn_on()

