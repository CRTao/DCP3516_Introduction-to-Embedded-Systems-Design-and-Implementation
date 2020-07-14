import cv2

class Camera(object):
	def __init__(self):
		if cv2.__version__.startswith('2'):
			PROP_FRAME_WIDTH = cv2.cv.CV_CAP_PROP_FRAME_WIDTH
			PROP_FRAME_HEIGHT = cv2.cv.CV_CAP_PROP_FRAME_HEIGHT
		elif cv2.__version__.startswith('3'):
			PROP_FRAME_WIDTH = cv2.CAP_PROP_FRAME_WIDTH
			PROP_FRAME_HEIGHT = cv2.CAP_PROP_FRAME_HEIGHT
		self.video = cv2.VideoCapture(0)
		self.video.set(PROP_FRAME_WIDTH,320)
		self.video.set(PROP_FRAME_WIDTH,240)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()
		ret, jpeg = cv2.imencode('.jpg',image)
		return jpeg.tostring()
