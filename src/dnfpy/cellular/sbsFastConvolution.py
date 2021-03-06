from dnfpy.cellular.sbsFastMap import SbsFastMap
from dnfpy.core.map2D import Map2D
from dnfpy.cellular.bsRsdnfConvolution import normalizeProba,normalizeIntensity

class SbsFastConvolution(Map2D):
    """
    Children needed: "activation" with map of 0 and 1
    """
    def __init__(self,name,size,dt=0.1,sizeStream=2000,pSpike=0.01,routerType="orRouter",
                 precisionProba=31,
                 iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.4,alpha=10,
                 iExc_=1.,iInh_=1.,pInh_=0.,pExc_=0.,reproductible=True,
                 nstep=1,
                 **kwargs):
        super().__init__(name,size,dt=dt,
                sizeStream=sizeStream,pSpike=pSpike,routerType=routerType,
                precisionProba=precisionProba,nstep=nstep,
                iExc=iExc,iInh=iInh,pExc=pExc,pInh=pInh,alpha=alpha,
                iExc_=iExc_,iInh_=iInh_,pInh_=pInh_,pExc_=pExc_,
                reproductible=reproductible, **kwargs)
        print(sizeStream,pSpike)
        self.inh = SbsFastMap(name+"_inh",size,dt=dt,
                    sizeStream=sizeStream,probaSpike=pSpike,probaSynapse=pInh_,
                              reproductible=reproductible,precisionProba=precisionProba,
                              nstep=nstep)
        self.exc = SbsFastMap(name+"_exc",size,dt=dt,
                    probaSpike=pSpike,sizeStream=sizeStream,probaSynapse=pExc_,
                              reproductible=reproductible,precisionProba=precisionProba,
                              nstep=nstep)

        self.addChildren(inhMap = self.inh,excMap = self.exc)


    def _compute(self,inhMap,excMap,iInh_,iExc_):
        self._data = excMap *  iExc_ - inhMap * iInh_

    def resetData(self):
        pass #no need to reset, it is automatically reset before computation

    def _onParamsUpdate(self,size,alpha,sizeStream,iExc,iInh,pExc,pInh,pSpike):
        pExc_ = normalizeProba(pExc,size)
        pInh_ = normalizeProba(pInh,size)

        iExc_ = normalizeIntensity(iExc,size,alpha,sizeStream,pSpike)
        iInh_ = normalizeIntensity(iInh,size,alpha,sizeStream,pSpike)
        #print("size : %s"%size)
        #print("pExc %s, pInh %s, iExc %s, iInh %s"%(pExc,pInh,iExc,iInh))
        #print("pExc_ %s, pInh_ %s, iExc_ %s, iInh_ %s"%(pExc_,pInh_,iExc_,iInh_))


        return dict(pExc_=pExc_,pInh_=pInh_,iExc_=iExc_,iInh_=iInh_)

    def _childrenParamsUpdate(self,sizeStream,pSpike,pInh_,pExc_,
                              precisionProba,nstep):
        self.exc.setParams(sizeStream=sizeStream,probaSpike=pSpike,probaSynapse=pExc_,
                           precisionProba=precisionProba,nstep=nstep)
        self.inh.setParams(sizeStream=sizeStream,probaSpike=pSpike,probaSynapse=pInh_,
                           precisionProba=precisionProba,nstep=nstep)


    def _onAddChildren(self,**kwargs):
        if "activation" in kwargs.keys():
            actMap = kwargs.get("activation")
            self.exc.addChildren(activation=actMap)
            self.inh.addChildren(activation=actMap)

