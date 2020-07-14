
# Import packages
import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import argparse
import sys
from utils import label_map_util
from utils import visualization_utils as vis_util

class ODP(object):
    def __init__(self):
        print("Setting Up...")
        camera_type = 'picamera'
        
        sys.path.append('..')
        MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'
        CWD_PATH = os.getcwd()
        PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

        PATH_TO_LABELS = os.path.join(CWD_PATH,'data','mscoco_label_map.pbtxt')

        NUM_CLASSES = 90

        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)

        # Load the Tensorflow model into memory.
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            self.sess = tf.Session(graph=detection_graph)
        
        self.image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        self.detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        self.detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        
        IM_WIDTH = 320
        IM_HEIGHT = 240
        
        self.camera = PiCamera()
        self.camera.resolution = (IM_WIDTH,IM_HEIGHT)
        self.camera.framerate = 10
        self.rawCapture = PiRGBArray(self.camera, size=(IM_WIDTH,IM_HEIGHT))
        self.rawCapture.truncate(0)
        print("Setting Complete...")
    
    def __del__(self):
        self.camera.close()

    def getframe(self):
        # Set up camera constants

        self.camera.capture(self.rawCapture, 'rgb')

        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        frame = np.copy(self.rawCapture.array)
        frame.setflags(write=1)
        frame_expanded = np.expand_dims(frame, axis=0)

        # Perform the actual detection by running the model with the image as input
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: frame_expanded})

        # Draw the results of the detection (aka 'visulaize the results')
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            self.category_index,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.40)
            
        ret, jpeg = cv2.imencode('.jpg',frame)
        
        # All the results have been drawn on the frame, so it's time to display it.
        #cv2.imshow('Object detector', frame)
        return jpeg.tostring()

