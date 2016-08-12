from dnfpy.core.map2D import Map2D
import random
import sys
import numpy as np
from dnfpy.cellular.hardlib import HardLib

class SbsFastMap(Map2D):
        """

        CHILDREN NEEDED
        *"activation": an activation map with bool or int of value 0 or 1
        """
        class Params:
            PROBA_SPIKE=0
            SIZE_STREAM=1
            PROBA_SYNAPSE=2
            PRECISION_PROBA = 3
            NB_NEW_RANDOM_BIT = 4


        class Attributes:
            NB_BIT_RECEIVED=0
            ACTIVATED=1
            DEAD=2

        def __init__(self,name,size,dt=0.1,sizeStream=20,probaSpike=1.,
                     probaSynapse=1.,
                     precisionProba=31,
                     reproductible=True,
                     **kwargs):
            self.lib = HardLib(size,size,"cellsbsfast","rsdnfconnecter")
            super().__init__(name=name,size=size,dt=dt,
                                           sizeStream=sizeStream,
                                            probaSpike=probaSpike,
                                            probaSynapse=probaSynapse,
                                            precisionProba=precisionProba,
                                            reproductible=reproductible,
                                            **kwargs)
            #print(sizeStream,probaSpike,precisionProba)


        def _compute(self,size,activation):
            self.lib.setArrayAttribute(self.Attributes.ACTIVATED,activation)
            self.lib.preCompute()
            self.lib.step()
            self.lib.getArrayAttribute(self.Attributes.NB_BIT_RECEIVED,self._data)
            self.lib.reset()


        def reset(self):
            super(SbsFastMap,self).reset()
            size = self._init_kwargs['size']
            self._data = np.zeros((size,size),dtype=np.intc)
            if self.lib:
                self.lib.reset()

        def _onParamsUpdate(self,sizeStream,probaSpike,probaSynapse,
                            precisionProba,reproductible):
            self.lib.setMapParam(self.Params.SIZE_STREAM,sizeStream)
            self.lib.setMapParam(self.Params.PROBA_SPIKE,probaSpike)
            self.lib.setMapParam(self.Params.PROBA_SYNAPSE,probaSynapse)
            self.lib.setMapParam(self.Params.PRECISION_PROBA,2**precisionProba-1)
            #print("params update")
            if reproductible:
                self.lib.initSeed(0)
            else:
                seed = random.randint(0, 1e10)
                self.lib.initSeed(seed)
            return {}
