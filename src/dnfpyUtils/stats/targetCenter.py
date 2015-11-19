import numpy as np
import dnfpy.core.utilsND as utils

from dnfpy.core.mapND import MapND
class TargetCenter(MapND):
        """
        Input: 
            inputMap (constructor)
            targetList (children)

            
        Output:
            the center of the followed track from target lsit


        """
        def __init__(self,name,inputMap,inputSize,dim=1,dt=0.1,wrap=True,**kwargs):
                super().__init__(name=name,size=0,dim=dim,dt=dt,wrap=wrap,inputSize=inputSize,**kwargs)
                self.inputMap = inputMap


        def _compute(self,targetList,inputSize):
            assert(len(targetList) == 1) #this is designed for only one target
            target =  self.inputMap.getTracks()[targetList[0]]
            self._data = np.array(target.getCenter())/inputSize


        def getViewSpace(self):
                dim = self.getArg('dim')
                return (1,)*dim





