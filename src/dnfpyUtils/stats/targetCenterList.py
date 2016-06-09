import numpy as np
import dnfpy.core.utils as utils

from dnfpyUtils.stats.trajectory import Trajectory
class TargetCenterList(Trajectory):
        """
        Input: 
            inputMap (constructor)
            targetList (children)

            
        Output:
            the center of the followed track from target lsit


        """
        def __init__(self,name,inputMap,inputSize,dim=1,dt=0.1,wrap=True,**kwargs):
                super().__init__(name=name,dim=dim,dt=dt,wrap=wrap,inputSize=inputSize,**kwargs)
                self.inputMap = inputMap
               
        def reset(self):
            super().reset()
            dim = self.getArg('dim')
            self._data = [(np.nan,)*dim]


        def _compute(self,targetList,inputSize):
            li = []
            for i in range(len(targetList)):
                target =  self.inputMap.getTracks()[targetList[i]]
                li.append(np.array(target.getCenter())/inputSize)
            self._data = li
            self.trace.append(np.copy(self._data))


        def getViewSpace(self):
                dim = self.getArg('dim')
                return (1,)*dim





