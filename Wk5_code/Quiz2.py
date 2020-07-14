import RPi.GPIO as GPIO
import time
import smbus
import string

LED_pin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_pin,GPIO.OUT)

def getSignedNumber(number):
    if number & (1 << 15):
        return number | ~65535
    else:
        return number & 65535

i2c_bus=smbus.SMBus(1)
i2c_address=0x69
i2c_bus.write_byte_data(i2c_address,0x20,0x0F)
i2c_bus.write_byte_data(i2c_address,0x23,0x20)

try:
    while True:
        i2c_bus.write_byte(i2c_address,0x2C)
        Z_L = i2c_bus.read_byte(i2c_address)
        i2c_bus.write_byte(i2c_address,0x2D)
        Z_H = i2c_bus.read_byte(i2c_address)
        Z = Z_H << 8 | Z_L
        Z = getSignedNumber(Z)
	print(Z)
	if Z < -800 :
            print("LED is on")
            GPIO.output(LED_pin,GPIO.HIGH)
        elif Z > 800:
	    print("LED is off")
            GPIO.output(LED_pin,GPIO.LOW)
        time.sleep(0.5)
except KeyboardInterrupt:
    print "Exception: KeyboardInterrput"

finally:
    GPIO.cleanup()

