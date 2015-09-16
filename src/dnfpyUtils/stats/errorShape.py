from dnfpy.core.map2D import Map2D
import numpy as np

class ErrorShape(Map2D):
    """
    Input : 
    1) shapeMap : map with the expected shape of the activation
    2) activationMap : map of the activation

    Output:
    error = sum(|shape - act|/(shape.size**2))
    mean = mean(error)

    Limit cases:
    If shapeMap == 0:
        error = 10
    If activationMap == 0:
        error = 10

    """
    def __init__(self,name,size=0,dt=0.1,
                 **kwargs):
        super(ErrorShape,self).__init__(name=name,size=size,dt=dt,
                **kwargs)
        self.meanErrorSave = []
        self.setArg(mean=0.0)

    def _compute(self,shapeMap,activationMap):
        if np.all(shapeMap == 0):
            error = 10 #ther is no shape
        elif np.all(activationMap == 0):
            error = 10
            self.meanErrorSave.append(error)
            self.setArg(mean=np.mean(self.meanErrorSave))
        else:
            error = np.sum(np.abs(shapeMap - activationMap)/(shapeMap.shape[0]*shapeMap.shape[1]))*100
            self.meanErrorSave.append(error)
            self.setArg(mean=np.mean(self.meanErrorSave))

        self._data = error

