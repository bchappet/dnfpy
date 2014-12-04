from dnfpy.core.map2D import Map2D
import numpy as np
import cv2

class WebcamMap(Map2D):
   """
       Capture image from webcam
   """
   def __init__(self,size,numDevice=0,**kwargs):
        super(WebcamMap,self).__init__(size,numDevice=numDevice,**kwargs)
        self.capture = cv2.VideoCapture(numDevice)


   def _compute(self,size):
        ret,frame = self.capture.read()
        array = cv2.resize(frame,(size,size))
        self._data =  array

