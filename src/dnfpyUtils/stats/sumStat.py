from dnfpyUtils.stats.trajectory import Trajectory
import numpy as np

class SumStat(Trajectory):
    """
    Compute sum of given map
    child map 
    """
    def  _compute(self,map):
        self._data = np.sum(map)
        self.trace.append(self._data)



