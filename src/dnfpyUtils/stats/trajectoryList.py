import numpy as np
from dnfpyUtils.stats.trajectory import Trajectory

class TrajectoryList(Trajectory):
    """
    Abstract class for trajectory with a list of values
    The list length is not constant
    The aim is to be able to display every value with different color
    """
    def getMean(self):
        sum = 0
        for t in self.trace:
            mean = np.nanmean(t)
            sum += 0.0 if np.isnan(mean) else mean
        return sum/len(self.trace)

    def getRMSE(self):
        assert(False)#TODO
        return np.sqrt(np.nanmean(self.trace))


