from dnfpy.core.map2D import Map2D
import numpy as np
from dnfpyUtils.stats.trajectory import Trajectory

class ActivationSize(Trajectory):
    """
    Param :
        dx
    Input : 
    1) activationMap : map of the activation

    Output:
        a

    Limit cases:
    If only step activation for now

    """
    def _compute(self,act,dx):
        self._data = np.sum(act)*dx
        self.trace.append(self._data)





