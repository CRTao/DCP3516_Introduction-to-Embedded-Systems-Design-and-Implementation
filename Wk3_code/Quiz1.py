import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

sensor = 11
pin = 4
LED_pin = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_pin,GPIO.OUT)

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if temperature > 23:
            print("High temperature : %.1f" %temperature)
            GPIO.output(LED_pin,GPIO.HIGH)
            time.sleep(0.5)
        else:
            print("Low temerature : %.1f" %temperature)
            GPIO.output(LED_pin,GPIO.LOW)
            time.sleep(0.5)
except KeyboardInterrupt:
    print "Exception: KeyboardInterrput"

finally:
    GPIO.cleanup()
