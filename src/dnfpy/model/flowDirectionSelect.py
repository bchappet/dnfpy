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
                #find the center of the activity bubble (max for now, TODO barycenter
                max = np.max(colorDNFAct)
                itemIndex = np.where(colorDNFAct==max)
                cx = itemIndex[0][0]
                cy = itemIndex[1][0]

                #average the optical flow direction 
                halfSample = round((sampleSize * globalSize )/2.)
                flowBGR_ROI = flowBGR[cx-halfSample:cx+halfSample,
                                        cy-halfSample:cy+halfSample,:]
                averageOpticalFlowColor = np.mean(flowBGR_ROI)


                #set self._data
                self._data = averageOpticalFlow
