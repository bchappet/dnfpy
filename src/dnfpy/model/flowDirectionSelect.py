import numpy as np
from dnfpy.core.map2D import Map2D
import cv2


class FlowDirectionSelect(Map2D):
    """
    Will give the average best color direction based on the average direction
    on the barycenter of the activity
    the size should be 1
    globalSize should be the one of flowBGR and colorDNFAct
    TODO make to maps: 
        1)AverageROI cx,cy,sampleSize -> value of average
        2)GetMaxCoord map -> cx,cy
    """
    def _compute(self,globalSize,flowBGR,colorDNFAct,sampleSize):
        nbAct = np.sum(colorDNFAct)
	self.reset()
	if nbAct > 0:
		mult0 = np.multiply(flowBGR[:,:,0],colorDNFAct)
		mult1 = np.multiply(flowBGR[:,:,1],colorDNFAct)
		mult2 = np.multiply(flowBGR[:,:,2],colorDNFAct)
		sum0 = np.sum(mult0)
		sum1 = np.sum(mult1)
		sum2 = np.sum(mult2)
		averageOpticalFlowColor = np.zeros((3))
		averageOpticalFlowColor = np.array([sum0/nbAct,sum1/nbAct,sum2/nbAct])

		#set self._data
		#transform in hsv
		mat = np.array([[averageOpticalFlowColor]],dtype=np.uint8)
		hsv = cv2.cvtColor(mat,cv2.COLOR_BGR2HSV)
		bgr2 = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
		self._data = hsv


    def reset(self):
        self._data = np.array([[[0,0,0]]],dtype=np.uint8)






