from dnfpy.core.map2D import Map2D
import numpy as np
from dnfpyUtils.stats.trajectoryList import TrajectoryList
import dnfpy.core.utils as utils

class ErrorDistSimpleList(TrajectoryList):
    """
    Input : 
    1) target : map with the expected coordinates list
    2) mesured : map with the mesured coordinates list
    3)sizeMap : size of the maps (construtor)

    Output:
    error = euclidian distance list

    Limit cases:
    If target == nan and mesured == nan:
        error =  0.0
    elsif mesured == nan:
        error =  1.0
    elsif target == nan:
        error = 1.0

    """

    def _compute(self,target,mesured,wrap):
        error = []
        #make sure that there is as many measuered as target
        mesured_full = []
        mesured_full.extend(mesured)
        for i in range(len(target) - len(mesured)):
            mesured_full.append(np.nan)

        for t,m in zip(target,mesured_full):
            if np.any(np.isnan(t)) and np.any(np.isnan(m)) :
                dist = 0.0
            elif np.any(np.isnan(t)) or np.any(np.isnan(m)) :
                dist = 1.0
            else:
                if wrap:
                    t = t % 1 
                    dist = utils.wrappedVector(t,m,1)
                else:
                    dist = t-m

            error.append(np.sqrt(np.sum(dist**2)))

        self._data = error
        self.trace.append(error)

