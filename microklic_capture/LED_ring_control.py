import board
import neopixel
import sys
import argparse

class LEDRing:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D18, 20)
     
    def turn_on(self):
     self.pixels.fill((255,255,255))
     
    def turn_off(self):
        self.pixels.fill((0,0,0))
    
    def turn_on_rgb(r,g,b,self):
        self.pixels.fill((r , g, b))
        
if __name__=='__main__':
    
    led_arr= LEDRing()
    if sys.argv[1] == 'on':
        led_arr.turn_on()
    if sys.argv[1] == 'off':
        led_arr.turn_off()
        