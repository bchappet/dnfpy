from dnfpy.core.map2D import Map2D
import numpy as np
from dnfpy.cellular.hardlib import HardLib

class NSpikeMap(Map2D):
        def __init__(self,name,size,dt=0.1,nspike=20,proba=1.,**kwargs):
            self.lib = HardLib(size,size,"cellnspike","nspikeconnecter")
            super(NSpikeMap,self).__init__(name=name,size=size,dt=dt,
                                           nspike=nspike,proba=proba,**kwargs)

        def _compute(self,size,activation):
            self.reset()
            self.lib.setArrayAttribute(1,activation)
            self.lib.step()
            self.lib.getArrayAttribute(0,self._data)


        def reset(self):
            size = self.getArg('size')
            self._data = np.zeros((size,size),dtype=np.intc)
            if self.lib:
                self.lib.reset()
                self.lib.getArrayAttribute(0,self._data)

        def _onParamsUpdate(self,nspike,proba):
            self.lib.setMapParam(0,nspike)
            for i in range(1,5):
                self.lib.setMapParam(i,proba)
            return {}
