from dnfpy.core.map2D import Map2D
from scipy.spatial import distance
from dnfpy.stats.statistic import Statistic
import numpy as np



ERROR = 1.
class ErrorDist(Statistic):
    def __init__(self,name,size=0,dt=0.1,sizeArray=20,canSwitch=True,
                 coherencyTime=1.,distMax=0.3,**kwargs):
        super(ErrorDist,self).__init__(name=name,size=size,dt=dt,
                sizeArray=sizeArray,
                canSwitch=canSwitch,distMax=distMax,
                coherencyTime=coherencyTime,
                **kwargs)
        self.meanErrorSave = []
        self.setArg(mean=0.0)

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
        self.meanErrorSave.append(np.sum(error))
        self.setArg(mean=np.mean(self.meanErrorSave))
        self._data = error

    def getTrace(self):
        return self.meanErrorSave
