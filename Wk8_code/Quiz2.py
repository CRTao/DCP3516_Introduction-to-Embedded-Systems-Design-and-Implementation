import time
import picamera

with picamera.PiCamera() as camera:
	camera.resolution = (640,480)
	camera.framerate = 24
	camera.start_preview()
	timestamp = int(time.time())
	camera.annotate_text = str(timestamp)
	time.sleep(2)
	camera.capture("/home/pi/Lab/Wk8_code/Quiz2/image_"+str(timestamp)+".jpg")

