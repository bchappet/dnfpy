import numpy as np
from dnfpy.core.map2D import Map2D
import cv2


class FlowDirectionSelect(Map2D):
	"""
	Will give the average best polar direction based on the average direction
	on the barycenter of the activity
	the size should be 1
	globalSize should be the one of optFlowDir and colorDNFAct
	"""
	def _compute(self,globalSize,flow,colorDNFAct,sampleSize):
                #find the center of the activity bubble (max for now, TODO barycenter
                max = np.max(colorDNFAct)
                itemIndex = np.where(colorDNFAct==max)
                cx = itemIndex[0][0]
                cy = itemIndex[1][0]


                #transform in polar
                mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])

                #average the optical flow direction 
                halfSample = round((sampleSize * globalSize )/2.)
                optFlowDir = np.multiply(
                        ang[cx-halfSample:cx+halfSample,
                        cy-halfSample:cy+halfSample],
                        mag[cx-halfSample:cx+halfSample,
                        cy-halfSample:cy+halfSample]
                        )
                averageOpticalFlow = np.mean(optFlowDir)


                #set self._data
                self._data = averageOpticalFlow
