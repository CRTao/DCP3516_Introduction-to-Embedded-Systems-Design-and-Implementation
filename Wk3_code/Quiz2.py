import RPi.GPIO as GPIO
import time

v = 343
TRIGGER_PIN = 16
ECHO_PIN = 18
LED_pin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIGGER_PIN,GPIO.OUT)
GPIO.setup(ECHO_PIN,GPIO.IN)
GPIO.setup(LED_pin,GPIO.OUT)

GPIO.output(LED_pin,GPIO.LOW)

def measure():
    GPIO.output(TRIGGER_PIN,GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN,GPIO.LOW)
    pulse_start = time.time()
    pulse_end = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()
    t = pulse_end - pulse_start
    d = t * v
    d = float(d/2)
    return d*100

def blink():
    GPIO.output(LED_pin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LED_pin,GPIO.LOW)
    time.sleep(1)

def fastblink():
    for i in range(1,4):
        GPIO.output(LED_pin,GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(LED_pin,GPIO.LOW)
        time.sleep(0.25)

try:
    while True:
        dis =  measure()
        if dis <= 5 :
            fastblink()
            print("Danger!! %f" %dis)
        elif dis > 5 and dis <= 30:
	    blink()
            print("Warning! %f" %dis)
        else :
            print("Safe %f" %dis) 
            time.sleep(2)
except KeyboardInterrupt:
    print "KeyboardInterrupt"
finally:
    GPIO.cleanup()


