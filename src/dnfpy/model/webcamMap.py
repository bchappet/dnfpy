from dnfpy.core.map2D import Map2D
import numpy as np
import cv2
import matplotlib.pyplot as plt

class WebcamMap(Map2D):
   """
       Capture image from webcam
   """
   def __init__(self,size,**kwargs):
        super(WebcamMap,self).__init__(size,**kwargs)
        self.capture = cv2.VideoCapture(0)


   def _compute(self,size):
        ret,frame = self.capture.read()
        array = cv2.resize(frame,(size,size))
        self._data =  array

