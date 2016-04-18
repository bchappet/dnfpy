from dnfpy.core.map2D import Map2D
from dnfpy.core.constantMap import ConstantMap
import random
import sys
import numpy as np
from dnfpy.cellular.hardlib import HardLib

class CasasField(Map2D):
        """

        CHildren needed aff
        """
        class Params:
            SIZE_POTENTIAL_STREAM=0 #int
            THRESHOLD=1         #int
            PROBA_EXC=2         #float
            PROBA_INH=3         #float
            PRECISION_PROBA=4   #int
            TAU=5               #float

        class SubParams:
            SIZE_STREAM = 0

        class Attributes:
            POTENTIAL=0
            NB_ACT=1
            STIM=2
            NB_BIT_EXC=3
            NB_BIT_INH=4
            NB_BIT_STIM=5


        def __init__(self,name,size,dt=0.1,sizeStream=1000,
                     pExc=1.,pInh=1.,tau=1.0,th=25,
                     precisionProba=30,
                     reproductible=True,
                     **kwargs):
            self.lib = HardLib(size,size,"neuroncasasfast","rsdnfconnecter2layer")
            super().__init__(name=name,size=size,dt=dt,
                                           sizeStream=sizeStream,
                                            pExc=pExc,pInh=pInh,
                                            precisionProba=precisionProba,
                                            tau=tau,th=th,
                                            reproductible=reproductible,
                                            **kwargs)

            self.act = ConstantMap("Activation",size,np.zeros((size,size),dtype=np.intc))
            self.latExc = ConstantMap("LateralExc",size,np.zeros((size,size),dtype=np.intc))
            self.latInh = ConstantMap("LateralInh",size,np.zeros((size,size),dtype=np.intc))


        def _compute(self,aff):
            self.lib.setArrayAttribute(self.Attributes.STIM,aff)
            self.lib.preCompute()
            self.lib.compute()
            self.lib.getArrayAttribute(self.Attributes.POTENTIAL,self._data)
            self._data = self._data*2-1 #convert bs to [-1,1]

            self.lib.getArrayAttribute(self.Attributes.NB_ACT,self.act._data)
            self.lib.getArrayAttribute(self.Attributes.NB_BIT_EXC,self.latExc._data)
            self.lib.getArrayAttribute(self.Attributes.NB_BIT_INH,self.latInh._data)



        def getActivation(self):
            return self.act


        def getArrays(self):
            return [
                self.act,
                self.latExc,
                self.latInh,
            ]


        def reset(self):
            super().reset()
            if self.lib:
                self.lib.reset()

        def _onParamsUpdate(self,sizeStream,pExc,pInh,
                            precisionProba,reproductible,tau,th):
            self.lib.setMapParam(self.Params.SIZE_POTENTIAL_STREAM,sizeStream)
            self.lib.setMapSubParam(self.SubParams.SIZE_STREAM,sizeStream)
            self.lib.setMapParam(self.Params.THRESHOLD,th)
            self.lib.setMapParam(self.Params.PROBA_EXC,pExc)
            self.lib.setMapParam(self.Params.PROBA_INH,pInh)
            #self.lib.setMapSubParam(self.Params.PRECISION_PROBA,2**precisionProba-1) #TODO std_outof range
            self.lib.setMapParam(self.Params.TAU,tau)
            if reproductible:
                self.lib.initSeed(255)
            else:
                seed = random.randint(0, 1e10)
                self.lib.initSeed(seed)
            return {}

if __name__ == "__main__":
    size = 11
    stim = np.zeros((size,size),np.float32)
    aff = ConstantMap('aff',size,stim)
    map = CasasField("uut",size,pExc=0.91,pInh=0.95)
    map.addChildren(aff=aff)
    #for i in range(100):
    #    map.compute();
    #print(map.getData())

    stim[size//2,size//2] = 0.99
    map.compute();
    print(map.getData())
    print(map.act.getData())

    for i in range(3):
        print(i)
        map.compute();
        print(map.getData())
        print(map.act.getData())
        print(map.latExc.getData())
        print(map.latInh.getData())

