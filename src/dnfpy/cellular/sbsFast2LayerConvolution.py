from dnfpy.cellular.hardlib import HardLib
from dnfpy.core.map2D import Map2D
from dnfpy.cellular.bsRsdnfConvolution import normalizeProba,normalizeIntensity
import numpy as np
import random
import sys

class SbsFast2LayerConvolution(Map2D):
    class Params:
            PROBA_SPIKE=0
            SIZE_STREAM=1
            PROBA_SYNAPSE=2
            PRECISION_PROBA = 3
            PROBA_SYNAPSE_INH = 4
            SHIFT = 5
            NB_SHARED_BIT = 6

    class Attributes:
            NB_BIT_RECEIVED=0
            ACTIVATED=1
            DEAD=2
            NB_BIT_INH_RECEIVED=3

    """
    Children needed: "activation" with map of 0 and 1
    """
    def __init__(self,name,size,dt=0.1,sizeStream=2000,pSpike=0.01,routerType="orRouter",
                 precisionProba=31,
                 iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.4,alpha=10,
                 iExc_=1.,iInh_=1.,pInh_=0.,pExc_=0.,reproductible=True,
                 nstep=1,shift=5,nbSharedBit=31,
                 **kwargs):
        self.lib = HardLib(size,size,"cellsbsfast2","rsdnfconnecter2layer")
        super(SbsFast2LayerConvolution,self).__init__(name,size,dt=dt,
                sizeStream=sizeStream,pSpike=pSpike,routerType=routerType,
                precisionProba=precisionProba,nstep=nstep,
                iExc=iExc,iInh=iInh,pExc=pExc,pInh=pInh,alpha=alpha,
                iExc_=iExc_,iInh_=iInh_,pInh_=pInh_,pExc_=pExc_,
                reproductible=reproductible,
                shift=shift,nbSharedBit=nbSharedBit,
                                                      **kwargs)



    def _compute(self,activation,iInh_,iExc_):
        self.lib.setArrayAttribute(self.Attributes.ACTIVATED,activation)
        self.lib.preCompute()
        self.lib.step()
        self.lib.getArrayAttribute(self.Attributes.NB_BIT_RECEIVED,self.excMap)
        self.lib.getArrayAttribute(self.Attributes.NB_BIT_INH_RECEIVED,self.inhMap)
        self.lib.reset()
        self._data = self.excMap *  iExc_ - self.inhMap * iInh_

    def reset(self):
            super(SbsFast2LayerConvolution,self).reset()
            size = self._init_kwargs['size']
            self._data = np.zeros((size,size),dtype=np.intc)
            self.excMap = np.zeros((size,size),dtype=np.intc)
            self.inhMap = np.zeros((size,size),dtype=np.intc)
            if self.lib:
                self.lib.reset()



    def resetData(self):
        pass #no need to reset, it is automatically reset before computation

    def _onParamsUpdate(self,size,alpha,sizeStream,iExc,iInh,pExc,pInh,pSpike,
                        precisionProba,reproductible,shift,nbSharedBit):
        pExc_ = normalizeProba(pExc,size)
        pInh_ = normalizeProba(pInh,size)

        iExc_ = normalizeIntensity(iExc,size,alpha,sizeStream,pSpike)
        iInh_ = normalizeIntensity(iInh,size,alpha,sizeStream,pSpike)
        #print("size : %s"%size)
        #print("pExc %s, pInh %s, iExc %s, iInh %s"%(pExc,pInh,iExc,iInh))
        #print("pExc_ %s, pInh_ %s, iExc_ %s, iInh_ %s"%(pExc_,pInh_,iExc_,iInh_))

        self.lib.setMapParam(self.Params.SIZE_STREAM,sizeStream)
        self.lib.setMapParam(self.Params.PROBA_SPIKE,pSpike)
        self.lib.setMapParam(self.Params.PROBA_SYNAPSE,pExc_)
        self.lib.setMapParam(self.Params.PROBA_SYNAPSE_INH,pInh_)
        self.lib.setMapParam(self.Params.PRECISION_PROBA,2**precisionProba-1)
        self.lib.setMapParam(self.Params.SHIFT,shift)
        self.lib.setMapParam(self.Params.NB_SHARED_BIT,nbSharedBit)
        if reproductible:
             self.lib.initSeed(0)
        else:
            seed = random.randint(0,1000000 )
            self.lib.initSeed(seed)


        return dict(pExc_=pExc_,pInh_=pInh_,iExc_=iExc_,iInh_=iInh_)
