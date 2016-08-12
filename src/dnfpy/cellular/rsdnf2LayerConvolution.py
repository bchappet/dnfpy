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

    class Reg:
        ACTIVATED=0
        NB_BIT_RECEIVED=1
        NB_BIT_INH_RECEIVED=2


    class SubReg:
        BUFFER = 0
        SPIKE_OUT = 1


    """
    Children needed: "activation" with map of 0 and 1
    """
    def __init__(self,name,size,dt=0.1,nspike=20,precisionProba=31,
                 iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.4,alpha=10,
                 iExc_=1.,iInh_=1.,pInh_=0.,pExc_=0.,reproductible=True,
                 nstep=1,shift=4,clkRatio = 50,
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
        self.excMap = np.zeros((size,size),dtype=np.intc)
        self.inhMap = np.zeros((size,size),dtype=np.intc)



    def _compute(self,activation,iInh_,iExc_):
        self._compute2(activation,iInh_,iExc_)

    def _compute2(self,activation,iInh_,iExc_):
        if self.newActivation:
            self.newActivation = False
            self.setActivation(activation)

        self.lib.preCompute()
        self.lib.step()
        self.lib.getRegArray(self.Reg.NB_BIT_RECEIVED,self.excMap)
        self.lib.getRegArray(self.Reg.NB_BIT_INH_RECEIVED,self.inhMap)
        self._data = self.excMap *  iExc_ - self.inhMap * iInh_

    def setActivation(self,activation):
        self.lib.setRegArray(self.Reg.ACTIVATED,activation)
        self.lib.synch()

    def reset(self):
        if self.lib:
            self.lib.reset()
        super().reset()
        size = self.getArg('size')
        self.newActivation = True #true when we want to get the new activation
        self.excMap = np.zeros((size,size),dtype=np.intc)
        self.inhMap = np.zeros((size,size),dtype=np.intc)


    def resetLat(self):
            """
            Reset the  NB_BIT_RECEIVED attribute of the map cells
            whenever the neuron potential is updated by reading
            self._data, the resetData method should be called
            In a fully pipelined BsRSDNF, the neuron potential
            is updated on every bit reception, the resetData is the called
            at every computation
            """
            size = self.getArg('size')
            self.lib.setRegArray(self.Reg.NB_BIT_RECEIVED, \
                                       np.zeros((size,size),dtype=np.intc))
            self.lib.setRegArray(self.Reg.NB_BIT_INH_RECEIVED, \
                                       np.zeros((size,size),dtype=np.intc))
            #reset buffer
            zeros = np.zeros((size,size,8),dtype=np.intc)
            self.lib.setArraySubState(self.SubReg.BUFFER,zeros)
            self.lib.setArraySubState(self.SubReg.SPIKE_OUT,zeros)
            self.lib.synch()
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
        print(newDt)
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





