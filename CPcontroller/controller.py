# Python serial controller for the Creality 5
import serial
import numpy as np
from time import sleep


class cp_control(object):
    '''
    Motion controller for scanning microscope based on the Creality Ender
    '''

    def __init__(self,port,baudrate):
        self.port = port
        self.baudrate = baudrate
        self.speed = 2000
        self.precision = 0.01
        self.homed = 0
        
    def setSpeed(self,speedval):
        self.speed = speedval

    def setPrecision(precision):
        self.precision = precision
        
    def connect(self):
        self.sock =  serial.Serial(self.port,self.baudrate)

    def home(self):
        print('Homing')
        self.sock.write('G28\n'.encode())
        while not self.homed:
            grbl_out = (self.sock.readline().decode()).strip()
            if grbl_out.find('X:0.00 Y:0.00') == -1:
                pass
            else:
                self.homed = 1
        print('Homed')
        return self.homed
        
    def getPosition(self):
        if self.homed:
            posstatus = self.sock.write('M114\n'.encode())
            gotposition = 0
            while not gotposition:
                current_position = self.sock.readline().decode().strip()
                if current_position == 'ok':
                    gotposition = 0
                elif not current_position.find('busy') == -1:
                    gotposition = 0
                else:
                    gotposition = 1
            xval = float(current_position[current_position.find('X')+2:current_position.find('Y')-1])
            yval = float(current_position[current_position.find('Y')+2:current_position.find('Z')-1])
            zval = float(current_position[current_position.find('Z')+2:current_position.find('E')-1])
            return xval, yval, zval
        print('Not yet homed')

    def in_position(self,setpoint, precision):
        xval, yval, zval = self.getPosition()
        if np.abs(setpoint[0]-xval) < self.precision and np.abs(setpoint[1]-yval) < self.precision and np.abs(setpoint[2]-zval) < self.precision:
            return True
        else:
            return False

    def inc(self,x_val,y_val,z_val):
        if self.homed:
            xval, yval, zval = self.getPosition()
            gcode = 'G1X'+str(xval+x_val)+'Y'+str(yval+y_val)+'Z'+str(zval+z_val)+'F'+str(self.speed)+'\n'
            self.sock.write(gcode.encode())
            if self.in_position([xval+x_val, yval+y_val, zval+z_val],self.precision):
                return self.getPosition()
        print('Not yet homed')

    def pos(self,x_val,y_val,z_val):
        if self.homed:
            gcode = 'G1X'+str(x_val)+'Y'+str(y_val)+'Z'+str(z_val)+'F'+str(self.speed)+'\n'
            self.sock.write(gcode.encode())
            if self.in_position([x_val,y_val,z_val],self.precision):
                return x_val, y_val, z_val
            else:
                return 'Failed to Move'
        print('Not yet homed')
        
    def close(self):
        self.sock.close()
        
        
class panel_control(object):
    '''
    Controller for light panel. Uses values from 0 to 255
    '''
    def __init__(self,port,baudrate):
        self.port = port
        self.baudrate = baudrate

    def connect(self):
        self.sock =  serial.Serial(self.port,self.baudrate)

    def pv(self,input_value):
        if input_value > 255:
            input_value = 255
        if input_value < 0:
            input_value = 0
        p_level = '{:03d}\n'.format(input_value)
        self.sock.write(p_level.encode())
        
    def close(self):
        self.sock.close()


