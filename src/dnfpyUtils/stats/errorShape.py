from dnfpy.core.map2D import Map2D
import numpy as np
from dnfpyUtils.stats.trajectory import Trajectory

class ErrorShape(Trajectory):
    """
    Input : 
    1) shapeMap : map with the expected shape of the activation
    2) activationMap : map of the activation

    Output:
    error = sum(|shape - act|/(shape.size**dim))

    Limit cases:
    If shapeMap == 0:
        error =  np.nan 
    If activationMap == 0:
        error =  np.nan

    """

    def _compute(self,shapeMap,activationMap):
        if np.all(shapeMap == 0):
            error = np.nan
        elif np.all(activationMap == 0):
            error = np.nan
        else:
            #error = np.sum(np.power(shapeMap*10 - activationMap,2)/(shapeMap.shape[0]*shapeMap.shape[1]*np.sum(shapeMap)))*100
            #error = np.sum(shapeMap == activationMap)/np.sum(shapeMap)
            outsideAct = np.sum((shapeMap - activationMap) == -1)
            badAct = (np.sum(shapeMap == 1) - np.sum(activationMap[shapeMap == 1]))
            error = (badAct+outsideAct) / np.sum(shapeMap) * 2

        self._data = error
        self.trace.append(error)

