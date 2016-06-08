import numpy as np
from dnfpyUtils.stats.trajectory import Trajectory

class TrajectoryList(Trajectory):
    """
    Abstract class for trajectory with a list of values
    The list length is not constant
    The aim is to be able to display every value with different color
    """
    def __getMean_old(self):
        sum = 0
        for t in self.trace:
            mean = np.nanmean(t)
            sum += 0.0 if np.isnan(mean) else mean
        return sum/len(self.trace)

    def getMean(self):
        tracei = [[] for i in range(10)]
        meani = [np.nan for i in range(10)]
        for t in self.trace:
            for i  in range(len(t)):
                tracei[i].append(t[i])
        for i in range(len(tracei)):
            if len(tracei[i]) > 0:
                meani[i] = np.nanmean(tracei[i])
        return np.nanmean(meani)

    def getRMSE(self):
        assert(False)#TODO
        return np.sqrt(np.nanmean(self.trace))


