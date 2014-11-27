from dnfpy.core.map2D import Map2D
import numpy as np
import cv2
import matplotlib.pyplot as plt

class WebcamMap(Map2D):
    def __init__(self,size,**kwargs):
        super(WebCamMap,self).__init__(size,**kwargs)
        self.capture = cv2.VideoCapture(0)


    def _compute(self,size):
        ret,frame = self.capture.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        array = cv2.resize(gray,(size,size))
        array = self.__invert(array)
        self._data =  self.__normalize(array)

    def __normalize(self,array):
        """
            Normalize between 0-1
        """
        return (array*1.0-np.min(array))/(np.max(array)-np.min(array))
    def __invert(sel,array):
        """
            Invert the colors
        """
        return 255 - array
