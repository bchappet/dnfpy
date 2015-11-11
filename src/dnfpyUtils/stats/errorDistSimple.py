from dnfpy.core.map2D import Map2D
import numpy as np
from dnfpyUtils.stats.trajectory import Trajectory
import dnfpy.core.utilsND as utils

class ErrorDistSimple(Trajectory):
    """
    Input : 
    1) target : map with the expected coordinates
    2) mesured : map with the mesured coordinates
    3)sizeMap : size of the maps (construtor)

    Output:
    error = euclidian distance 

    Limit cases:
    If shapeMap == nan:
        error =  np.nan 
    If activationMap == nan:
        error =  np.nan

    """

    def _compute(self,target,mesured,wrap):
        if wrap:
            target = target % 1 
            dist = utils.wrappedVector(target,mesured,1)
        else:
            dist = target-mesured


        error = np.sqrt(np.sum(dist**2))

        self._data = error
        self.trace.append(error)

