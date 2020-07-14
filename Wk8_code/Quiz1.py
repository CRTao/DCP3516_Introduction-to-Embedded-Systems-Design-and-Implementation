import time
import picamera
import schedule

def Photo1min():
	print("Run Photo1min")
	camera = picamera.PiCamera()
	camera.start_preview()
	try:
		for i,filename in enumerate(camera.capture_continuous("/home/pi/Lab/Wk8_code/Quiz1/image{timestamp:%y%m%d_%H-%M-%S}.jpg")):
			print(filename)
			time.sleep(1)
			if i == 9:
				break
	finally:
		camera.stop_preview()

schedule.every().day.at("13:40").do(Photo1min)

while True:
	schedule.run_pending()
	print("Waiting..."+time.strftime("%y%m%d_%H:%M:%S"))
	time.sleep(1)
