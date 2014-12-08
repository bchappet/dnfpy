from dnfpy.core.map2D import Map2D
import cv2

import numpy as np



class OpticalFlowMap(Map2D):
        """
        The chidren map should be one channel
        """
        def __init__(self,name,size,dt=0.1):
                super(OpticalFlowMap,self).__init__(name,size,dt=dt)
                self.__prev = np.zeros((size,size))


        def _compute(self,img):
                img_255 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                flow = cv2.calcOpticalFlowFarneback(self.__prev,img_255,
                                0.5, 3, 15, 3, 5, 1.2, 0)
                self.__prev = img_255
                self._data=flow
