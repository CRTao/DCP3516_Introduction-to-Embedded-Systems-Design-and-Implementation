#!/usr/bin/python
'''
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# camera_face_detect.py
# Face detect from camera
#
# Author : Fletcher Heisler, Michael Herman, Jeremy Johnson
# Date   : 06/22/2014
# Origin : https://realpython.com/blog/python/face-detection-in-python-using-a-webcam/
# Usage  : python cfd.py haarcascade_frontalface_default.xml
'''
import sys
import cv2
import time


class CFD(object):
    def __init__(self):

        cascPath = './cars.xml'
        self.faceCascade = cv2.CascadeClassifier(cascPath)

        if cv2.__version__.startswith('2'):
            PROP_FRAME_WIDTH = cv2.cv.CV_CAP_PROP_FRAME_WIDTH
            PROP_FRAME_HEIGHT = cv2.cv.CV_CAP_PROP_FRAME_HEIGHT
            self.HAAR_FLAGS = cv2.cv.CV_HAAR_SCALE_IMAGE

        elif cv2.__version__.startswith('3'):
            PROP_FRAME_WIDTH = cv2.CAP_PROP_FRAME_WIDTH
            PROP_FRAME_HEIGHT = cv2.CAP_PROP_FRAME_HEIGHT
            self.HAAR_FLAGS = cv2.CV_FEATURE_PARAMS_HAAR

        self.cap = cv2.VideoCapture(-1)
        self.cap.set(PROP_FRAME_WIDTH,320)
        self.cap.set(PROP_FRAME_WIDTH,240)


    def get_frame(self):

        ret, frame = self.cap.read()
        
        if ret is True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=self.HAAR_FLAGS
            )

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            if len(faces)>0:
                timestr = time.strftime("%Y%m%d-%H%M")
                cv2.imwrite('image/output_'+timestr+'.jpg', frame)
            # Display the resulting frame
            #cv2.imshow("preview", frame)
            cv2.putText(frame,"Detect {:>2d} Car".format(len(faces)),(10,30), cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)
            
            ret, jpeg = cv2.imencode('.jpg',frame)
            return jpeg.tostring()

    def __del__(self):
        self.cap.release()

