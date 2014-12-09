import numpy as np
from dnfpy.core.map2D import Map2D
import cv2


class FlowDirectionSelectHSV(Map2D):
    """
    Will give the average best color direction based on the average direction
    on the barycenter of the activity
    the size should be 1
    globalSize should be the one of flowBGR and colorDNFAct
    TODO make to maps: 
        1)AverageROI cx,cy,sampleSize -> value of average
        2)GetMaxCoord map -> cx,cy
    """
    def _compute(self,globalSize,flow,colorDNFAct,sampleSize):
        nbAct = np.sum(colorDNFAct)
	self.reset()
	if nbAct > 0:
            	mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])

		magROI = np.multiply(mag,colorDNFAct)
		angROI = np.multiply(ang,colorDNFAct)
		angSum = np.sum(angROI)
		magSum = np.sum(magROI)
		angMean = angSum/nbAct

		magMean = magSum/nbAct
		magMean = magMean * 255
		print("mag mean : %s"%magMean)

		
		
            	value = 255 if magMean > 255 else magMean
		hsv = np.array([[[angMean*180/np.pi/2,255,value]]],dtype=np.uint8)
		print("hsv : %s"%hsv)
		self._data = hsv


    def reset(self):
        self._data = np.array([[[0,0,0]]],dtype=np.uint8)






