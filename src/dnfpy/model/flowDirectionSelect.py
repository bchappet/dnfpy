import numpy as np
from dnfpy.core.map2D import Map2D


class FlowDirectionSelect(Map2D):
	"""
	Will give the average best cartesian direction based on the average direction
	on the barycenter of the activity
	the size should be 1
	globalSize should be the one of optFlowDir and colorDNFAct
	"""
	def _compute(globalSize,optFlowDir,colorDNFAct,sampleSize):
		
		#find the center of the activity bubble (max for now, TODO barycenter
		cx = 0
		cy = 0 
		max = np.max(colorDNFAct)
		
		
		
		
		#average the optical flow direction 
		halfSample = round((sampleSize * globalSize )/2.)
		averageOpticalFlow = np.mean(optFlowDir[cx-halfSample:cx+halfSample,
							cy-halfSample:cy+halfSample])
	

		#set self._data
		self._data = averageOpticalFlow
