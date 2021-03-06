from dnfpyUtils.stats.statistic import Statistic
import numpy as np

class Trajectory(Statistic):
    """
    Abstract class for trajectory
    """

    def __init__(self,name,dt=0.1,dim=0,**kwargs):
            super().__init__(name=name,size=0,dim=dim,dt=dt,**kwargs)
            self.trace = [] #save the trace
                

    def getViewData(self):
        return self._data#,self.getMean()

    def reset(self):
        super().reset()
        self.trace = []
        self._data = np.nan
    

    def getMean(self):
        return np.nanmean(self.trace)

    def getRMSE(self):
        return np.sqrt(np.nanmean(self.trace))

    def getCount(self):
        return np.sum(~np.isnan(self.trace))

    def getMax(self):
        return np.max(self.trace)

    def getPercentile(self,percent):
        return np.nanpercentile(self.trace,percent)
    
    def getMin(self):
        return np.min(self.trace)

    def getStd(self):
        return np.std(self.trace)
    
    def getTrace(self):
        """
        Return the time trace of the statistic
        """
        return self.trace
    


