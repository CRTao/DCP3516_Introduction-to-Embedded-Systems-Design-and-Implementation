import RPi.GPIO as GPIO
import time
import Adafruit_ADXL345
import math

LED_pin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_pin,GPIO.OUT)

accel = Adafruit_ADXL345.ADXL345()
k = 0

try:
    while True:
	x,y,z = accel.read()
	Ga = math.sqrt(x*x+y*y+z*z)
        print(Ga)
        if abs(Ga-230)<50 and k > 10: 
	    GPIO.output(LED_pin,GPIO.HIGH)
            print("Stable")
	    k=k+1
	elif abs(Ga-230)<50 and k<=10:
	    k=k+1
        else:
	    print("Unstable")
	    GPIO.output(LED_pin,GPIO.LOW)
            k=0
        time.sleep(0.5)
except KeyboardInterrupt:
    print "Exception: KeyboardInterrput"

finally:
    GPIO.cleanup()


