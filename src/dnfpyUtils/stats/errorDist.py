from dnfpy.core.map2D import Map2D
from dnfpyUtils.stats.trajectory import Trajectory
from scipy.spatial import distance
from dnfpyUtils.stats.statistic import Statistic
import numpy as np



ERROR = np.nan
class ErrorDist(Trajectory):

    def _compute(self,sizeArray,trackedTarget,clusterMap):
        error = []
        nbCluster = len(clusterMap)
        if nbCluster > 0 and -1 in clusterMap[0]:
            error = [ERROR] #to many activation
        else:
            for i in range(nbCluster):
                coorClust = clusterMap[i]/float(sizeArray)
                coorTarget = trackedTarget[i]/float(sizeArray)
                error.append(distance.euclidean(coorClust,coorTarget))
        self._data = error
        self.trace.append(np.sum(error))

