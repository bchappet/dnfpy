from dnfpy.core.map2D import Map2D
import sys
import random
import numpy as np
from dnfpy.cellular.hardlib import HardLib

class NSpikeMap(Map2D):
        """
        Activation type MUST be np.intc

        """
        def __init__(self,name,size,dt=0.1,nspike=20,proba=1.,
                     reproductible=True,**kwargs):
            self.lib = HardLib(size,size,"cellnspike","nspikeconnecter")
            super(NSpikeMap,self).__init__(name=name,size=size,dt=dt,
                                           nspike=nspike,proba=proba,
                                           reproductible=reproductible,
                                           **kwargs)
            if self.getArg('reproductible'):
                self.lib.initSeed(0)
            else:
                seed = random.randint(0, sys.maxint)
                self.lib.initSeed(seed)



        def _compute(self,size,activation):
            self.resetLib()
            self.lib.setArrayAttribute(1,activation)
            self.lib.step()
            self.lib.getArrayAttribute(0,self._data)

        def resetLib(self):
            self.lib.reset()
            self.lib.getArrayAttribute(0,self._data)


        def reset(self):
            super(NSpikeMap,self).reset()
            size = self._init_kwargs['size']
            self._data = np.zeros((size,size),dtype=np.intc)
            self.resetLib()


        def _onParamsUpdate(self,nspike,proba):
            self.lib.setMapParam(0,nspike)
            for i in range(1,5):
                self.lib.setMapParam(i,proba)
            return {}
