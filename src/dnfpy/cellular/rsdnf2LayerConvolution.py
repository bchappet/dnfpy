from dnfpy.cellular.hardlib import HardLib
from dnfpy.core.map2D import Map2D
from dnfpy.cellular.nSpikeConvolution import normalizeIntensity,normalizeProba
import numpy as np
import random
import sys

class Rsdnf2LayerConvolution(Map2D):
    class Params:
            #enum CellRsdnf_Params {NB_SPIKE=0,PROBA=1,PRECISION_PROBA=2};
            #enum CellRsdnf2_Params {PROBA_INH=3,PRECISION_RANDOM=4,NB_BIT_RANDOM=5,SHIFT=6};
            NB_SPIKE=0
            PROBA=1
            PRECISION_PROBA=2
            PROBA_INH=3
            PRECISION_RANDOM=4
            NB_BIT_RANDOM=5
            SHIFT=6

    class Attributes:
            NB_BIT_RECEIVED=0
            ACTIVATED=1
            DEAD=2
            NB_BIT_INH_RECEIVED=3

    """
    Children needed: "activation" with map of 0 and 1
    """
    def __init__(self,name,size,dt=0.1,nspike=20,precisionProba=31,
                 iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.4,alpha=10,
                 iExc_=1.,iInh_=1.,pInh_=0.,pExc_=0.,reproductible=True,
                 nstep=1,shift=0,clkRatio = 50,
                 **kwargs):
        self.lib = HardLib(size,size,"cellrsdnf2","rsdnfconnecter2layer")
        super().__init__(name,size,dt=dt,
                nspike=nspike,
                precisionProba=precisionProba,nstep=nstep,
                iExc=iExc,iInh=iInh,pExc=pExc,pInh=pInh,alpha=alpha,
                iExc_=iExc_,iInh_=iInh_,pInh_=pInh_,pExc_=pExc_,
                reproductible=reproductible,
                shift=shift,clkRatio=clkRatio,baseDt=dt,
                                                      **kwargs)
        self.newActivation = True #true when we want to get the new activation



    def _compute(self,activation,iInh_,iExc_):
        self._compute2(activation,iInh_,iExc_)

    def _compute2(self,activation,iInh_,iExc_):
        if self.newActivation:
            self.newActivation = False
            self.setActivation(activation)

        self.lib.preCompute()
        self.lib.step()
        self.lib.getArrayAttribute(self.Attributes.NB_BIT_RECEIVED,self.excMap)
        self.lib.getArrayAttribute(self.Attributes.NB_BIT_INH_RECEIVED,self.inhMap)
        self._data = self.excMap *  iExc_ - self.inhMap * iInh_

    def setActivation(self,activation):
        self.lib.setArrayAttribute(self.Attributes.ACTIVATED,activation)

    def reset(self):
            super().reset()
            self.resetLat()


    def resetLat(self):
        #we reset the data (NB_BIT_RECEIVED) of inh and exc when we integrate it
        #in the neural's potential
        size = self._init_kwargs['size']
        self._data = np.zeros((size,size),dtype=np.intc)
        self.excMap = np.zeros((size,size),dtype=np.intc)
        self.inhMap = np.zeros((size,size),dtype=np.intc)
        if self.lib:
            self.lib.reset()
        self.newActivation=True




    def _onParamsUpdate(self,size,alpha,nspike,iExc,iInh,pExc,pInh,
                        precisionProba,reproductible,shift,clkRatio):
        pExc_ = normalizeProba(pExc,size)
        pInh_ = normalizeProba(pInh,size)

        iExc_ = normalizeIntensity(iExc,size,alpha,nspike)
        iInh_ = normalizeIntensity(iInh,size,alpha,nspike)
#        print("size : %s"%size)
#        print("pExc %s, pInh %s, iExc %s, iInh %s"%(pExc,pInh,iExc,iInh))
#        print("pExc_ %s, pInh_ %s, iExc_ %s, iInh_ %s"%(pExc_,pInh_,iExc_,iInh_))

        self.lib.setMapParam(self.Params.NB_SPIKE,nspike)
        self.lib.setMapParam(self.Params.PROBA,pExc_)
        self.lib.setMapParam(self.Params.PROBA_INH,pInh_)
        self.lib.setMapParam(self.Params.PRECISION_PROBA,2**precisionProba-1)
        self.lib.setMapParam(self.Params.PRECISION_RANDOM,2**precisionProba-1)
        self.lib.setMapParam(self.Params.NB_BIT_RANDOM,precisionProba)
        self.lib.setMapParam(self.Params.SHIFT,shift)
        if reproductible:
            self.lib.initSeed(255)
        else:
            seed = random.randint(1, 10000000)
            self.lib.initSeed(seed)

        newDt = self.getArg('baseDt') / clkRatio
        self.setArg(dt=newDt)


        return dict(pExc_=pExc_,pInh_=pInh_,iExc_=iExc_,iInh_=iInh_)

if __name__ == "__main__":
    size = 100
    activation = np.zeros( ( size,size),np.bool_)
    uut = Rsdnf2LayerConvolution("uut",size,activation=activation)
    uut.reset()
    activation[size//2,size//2] = 1
    uut.setParams(pExc=1,pInh=1,nspike=20)
    activation[size//2-5:size//2+5,size//2-5:size//2+5] = 1
    uut.setParams(nspike=20)

    for i in range(100*20 + 200):
        uut.compute()
    data = uut.excMap
    assert(np.sum(data)==100*100*100*20 - 100*20)





