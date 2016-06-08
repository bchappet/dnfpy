from dnfpy.core.mapND import MapND
from dnfpyUtils.stats.barycenterMapList import BarycenterMapList
from dnfpyUtils.stats.trajectory import Trajectory
from dnfpyUtils.stats.clusterMapList import  getValidClusterList

class GoodFocus(Trajectory):
    def __init__(self,name,*args,**kwargs):
        super().__init__(name,*args,**kwargs)
        #self.focused = [] #trace for the focus : it is focused when the cluster are clean (no outliers)
        #                  and it is clean for convergenceTime seconds
        #self.cleanFocus = [] #boolean trace for clean focus
        #self.convergence = 0 #count until convergenceTime seconds

    def _compute(self,clusterList):
        validCoord,validClusterIndex= getValidClusterList (clusterList)
        self._data = (len(validCoord) == 1)
        self.trace.append(self._data)
        



