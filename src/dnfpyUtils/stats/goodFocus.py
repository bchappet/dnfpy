from dnfpy.core.mapND import MapND
from dnfpyUtils.stats.barycenterMapList import BarycenterMapList
from dnfpyUtils.stats.trajectory import Trajectory

class GoodFocus(Trajectory):
    def __init__(self,name,barycenterMap,*args,**kwargs):
        super().__init__(name,*args,**kwargs)
        self.barycenterMap = barycenterMap
        #self.focused = [] #trace for the focus : it is focused when the cluster are clean (no outliers)
        #                  and it is clean for convergenceTime seconds
        #self.cleanFocus = [] #boolean trace for clean focus
        #self.convergence = 0 #count until convergenceTime seconds

    def _compute(self,targetList):
        self._data = (len(targetList) == len(self.barycenterMap.getData())) and (self.barycenterMap.outsideAct[-1]==0)
        self.trace.append(self._data)
        



