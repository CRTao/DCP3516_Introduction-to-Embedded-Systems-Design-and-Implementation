import cv2
import sys


class Camera(object):
	def __init__(self):
		cascPath = "\home\pi\Lab\Wk9_code\haarcascade_frontalface_default.xml"
		self.facecascade = cv2.CascadeClassifier(cascPath)

		if cv2.__version__.startswith('2'):
			PROP_FRAME_WIDTH = cv2.cv.CV_CAP_PROP_FRAME_WIDTH
			PROP_FRAME_HEIGHT = cv2.cv.CV_CAP_PROP_FRAME_HEIGHT
			self.HAAR_FLAGS = cv2.cv.CV_HAAR_SCALE_IMAGE
		elif cv2.__version__.startswith('3'):
			PROP_FRAME_WIDTH = cv2.CAP_PROP_FRAME_WIDTH
			PROP_FRAME_HEIGHT = cv2.CAP_PROP_FRAME_HEIGHT
			self.HAAR_FLAGS = cv2.CV_FEATURE_PARAMS_HAAR
		self.cap = cv2.VideoCapture(0)

	def __del__(self):
		self.cap.release()

	def get_frame(self):
		
		ret, frame = self.cap.read()
		
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		faces = self.facecascade.detectMultiScale(
			gray,
			scaleFactor=1.1,
			minNeighbors=5,
			minSize=(30, 30),
			flags=self.HAAR_FLAGS
		)
	
		print "Found {0} faces!".format(len(faces))
	
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
	
		out, jpeg = cv2.imencode('.jpg',frame)
	
		return jpeg.tostring()

