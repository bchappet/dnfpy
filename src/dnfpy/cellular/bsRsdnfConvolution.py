from dnfpy.cellular.bsRsdnfMap import BsRsdnfMap
from dnfpy.core.map2D import Map2D


class BsRsdnfConvolution(Map2D):
    """
    Children needed: "activation" with map of 0 and 1
    """
    def __init__(self,name,size,dt=0.1,sizeStream=20,pSpike=1.,routerType="orRouter",
                 iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.4,alpha=10,
                 iExc_=1.,iInh_=1.,pInh_=0.,pExc_=0.,
                 **kwargs):
        super(BsRsdnfConvolution,self).__init__(name,size,dt=dt,
                sizeStream=sizeStream,pSpike=pSpike,routerType=routerType,
                iExc=iExc,iInh=iInh,pExc=pExc,pInh=pInh,alpha=alpha,
                 iExc_=iExc_,iInh_=iInh_,pInh_=pInh_,pExc_=pExc_,
                                               **kwargs)
        self.inh = BsRsdnfMap(name+"_inh",size,dt=dt,routerType=routerType,
                    sizeStream=sizeStream,probaSpike=pSpike,probaSynapse=pInh_)
        self.exc = BsRsdnfMap(name+"_exc",size,dt=dt,routerType=routerType,
                    probaSpike=pSpike,sizeStream=sizeStream,probaSynapse=pExc_)

        self.addChildren(inhMap = self.inh,excMap = self.exc)



    def _compute(self,inhMap,excMap,iInh_,iExc_,activation):
        self._data = excMap *  iExc_ - inhMap * iInh_
        #we reset the data (NB_BIT_RECEIVED) of inh and exc when we integrate it
        #in the neural's potential
        self.inh.resetData()
        self.exc.resetData()



    def _onParamsUpdate(self,size,alpha,sizeStream,iExc,iInh,pExc,pInh,pSpike):
        pExc_ = pExc**(1./(size))
        pInh_ = pInh**(1./(size))
        iExc_ = iExc/(size**2) * (40**2)/alpha * 1./(sizeStream*pSpike)
        iInh_ = iInh/(size**2) * (40**2)/alpha * 1./(sizeStream*pSpike)
#        print("pExc_ %s, pInh_ %s, iExc_ %s, iInh_ %s"%(pExc_,pInh_,iExc_,iInh_))


        return dict(pExc_=pExc_,pInh_=pInh_,iExc_=iExc_,iInh_=iInh_)

    def _childrenParamsUpdate(self,sizeStream,pSpike,pInh_,pExc_):
        self.exc.setParams(sizeStream=sizeStream,probaSpike=pSpike,probaSynapse=pExc_)
        self.inh.setParams(sizeStream=sizeStream,probaSpike=pSpike,probaSynapse=pInh_)

    def _onAddChildren(self,**kwargs):
        if "activation" in kwargs.keys():
            actMap = kwargs.get("activation")
            self.exc.addChildren(activation=actMap)
            self.inh.addChildren(activation=actMap)
