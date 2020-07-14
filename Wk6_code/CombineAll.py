import sys, os, thread, random, requests
from time import sleep
import RPi.GPIO as GPIO
import time
import Adafruit_ADXL345
import math
import smbus
import string
import numpy

def getSignedNumber(number):
    if number & (1 << 15):
        return number | ~65535
    else:
        return number & 6553

bus = smbus.SMBus(1)
addrHMC = 0x1e
i2c_bus=smbus.SMBus(1)
i2c_address=0x69
i2c_bus.write_byte_data(i2c_address,0x20,0x0F)
i2c_bus.write_byte_data(i2c_address,0x23,0x20)
accel = Adafruit_ADXL345.ADXL345()
xg = 1
yg = 1
zg = 1

def read_word(address, adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val

def read_a_data(xg,yg,zg):
    x,y,z = accel.read()
    Alpha = 0.5
    fxg = x*0.00390625
    fyg = y*0.00390625
    fzg = z*0.00390625

    ax = fxg*Alpha + (xg*(1-Alpha))
    xg = ax
    ay = fyg*Alpha + (yg*(1-Alpha))
    yg = ay
    az = fxg*Alpha + (zg*(1-Alpha))
    zg = az
    return ax,ay,az

def read_word_2c(address, adr):
    val = read_word(address, adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def main():

    bus.write_byte_data(addrHMC, 0, 0b01110000)  # Set to 8 samples @ 15Hz
    bus.write_byte_data(addrHMC, 1, 0b00100000)  # 1.3 gain LSb / Gauss 1090 (default)
    bus.write_byte_data(addrHMC, 2, 0b00000000)  # Continuous sampling

    while True:
        
        i2c_bus.write_byte(i2c_address,0x28)
        X_L = i2c_bus.read_byte(i2c_address)
        i2c_bus.write_byte(i2c_address,0x29)
        X_H = i2c_bus.read_byte(i2c_address)
        X = X_H << 8 | X_L
        i2c_bus.write_byte(i2c_address,0x2A)
        Y_L = i2c_bus.read_byte(i2c_address)
        i2c_bus.write_byte(i2c_address,0x2B)
        Y_H = i2c_bus.read_byte(i2c_address)
        Y = Y_H << 8 | Y_L
        i2c_bus.write_byte(i2c_address,0x2C)
        Z_L = i2c_bus.read_byte(i2c_address)
        i2c_bus.write_byte(i2c_address,0x2D)
        Z_H = i2c_bus.read_byte(i2c_address)
        Z = Z_H << 8 | Z_L
	ax,ay,az = read_a_data(xg,yg,zg)
        gx = getSignedNumber(X)
        gy = getSignedNumber(Y)
        gz = getSignedNumber(Z)
        mx = read_word_2c(addrHMC, 3)
        my = read_word_2c(addrHMC, 7)
        mz = read_word_2c(addrHMC, 5)
        '''
	print ("Acce_x: "+str(ax))
	print ("Acce_y: "+str(ay))
	print ("Acce_z: "+str(az))
	print ("Gyro_x: "+str(gx))
	print ("Gyro_y: "+str(gy))
	print ("Gyro_z: "+str(gz))
	print ("Magn_x: "+str(mx))
	print ("Magn_y: "+str(my))
	print ("Magn_z: "+str(mz))
	'''
	A = numpy.sqrt(ax*ax+ay*ay+az*az)
        print(A)
	time.sleep(1)

if __name__ == "__main__":
    main()
