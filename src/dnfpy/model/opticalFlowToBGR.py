from dnfpy.core.map2D import Map2D
import cv2
import numpy as np
class OpticalFlowToBGR(Map2D):
        """
        inputs:
            opticalFlow : raw dense optical flow
        outpus:
            bgr image with polar direction of mouvement converted en bgr

        """
        def __init__(self,name,size,dt=0.1):
            super(OpticalFlowToBGR,self).__init__(name,size,dt=dt)
            self.hsv = np.zeros((size,size,3),dtype=np.uint8)
            self.hsv[...,1] = 255

        def _compute(self,opticalFlow):
            mag, ang = cv2.cartToPolar(opticalFlow[...,0], opticalFlow[...,1])
            self.hsv[...,0] = ang*180/np.pi/2
            self.hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
            bgr = cv2.cvtColor(self.hsv,cv2.COLOR_HSV2BGR)
            self._data = bgr


