from dnfpy.core.map2D import Map2D
from scipy.spatial import distance
import numpy as np

class ErrorDist(Map2D):
    def __init__(self,name,size=0,dt=0.1,sizeArray=20,canSwitch=True,
                 coherencyTime=1.,distMax=0.2,**kwargs):
        super(ErrorDist,self).__init__(name=name,size=size,dt=dt,
                sizeArray=sizeArray,
                canSwitch=canSwitch,distMax=distMax,
                coherencyTime=coherencyTime,**kwargs)
        self.meanErrorSave = []
        self.setArg(mean=0.0)

    def _compute(self,sizeArray,trackedTarget,clusterMap):
        error = []
        for i in range(len(clusterMap)):
            coorClust = clusterMap[i]/float(sizeArray)
            coorTarget = trackedTarget[i]/float(sizeArray)
            error.append(distance.euclidean(coorClust,coorTarget))
            self._data = error
            self.meanErrorSave.append(error[0])
            self.setArg(mean=np.mean(self.meanErrorSave))

