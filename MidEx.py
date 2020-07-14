import time
import picamera
import sys
import Adafruit_DHT

sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

sensor = sensor_args[11]
pin = 4
    
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print()
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)


with picamera.PiCamera() as camera:
	camera.resolution = (640,480)
	camera.framerate = 24
	camera.start_preview()
	timestamp = int(time.time())
	camera.annotate_text = '0516320 >> Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
	time.sleep(2)
	camera.capture("/home/pi/Lab/Midterm/image_"+str(timestamp)+".jpg")

