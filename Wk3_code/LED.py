import RPi.GPIO as GPIO
import time

LED_pin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_pin,GPIO.OUT)

try:
    while True:
        print("LED is on")
        GPIO.output(LED_pin,GPIO.HIGH)
        time.sleep(1)
        print("LED is off")
        GPIO.output(LED_pin,GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    print "Exception: KeyboardInterrput"

finally:
    GPIO.cleanup()

