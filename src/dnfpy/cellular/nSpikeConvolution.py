from dnfpy.cellular.nSpikeMap import NSpikeMap
import numpy as np
from dnfpy.core.map2D import Map2D


class NSpikeConvolution(Map2D):
    """
    Children needed: "activation" with map of 0 and 1
    """
    def __init__(self,name,size,dt=0.1,nspike=20,
                 iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.4,alpha=10,
                 iExc_=1.,iInh_=1.,pInh_=0.,pExc_=0.,
                 **kwargs):
        super(NSpikeConvolution,self).__init__(name,size,dt=dt,nspike=nspike,
                iExc=iExc,iInh=iInh,pExc=pExc,pInh=pInh,alpha=alpha,
                 iExc_=iExc_,iInh_=iInh_,pInh_=pInh_,pExc_=pExc_,
                                               **kwargs)
        self.inh = NSpikeMap(name+"_inh",size,dt=dt,nspike=nspike,proba=pInh_)
        self.exc = NSpikeMap(name+"_exc",size,dt=dt,nspike=nspike,proba=pExc_)

        self.addChildren(inhMap = self.inh,excMap = self.exc)



    def _compute(self,inhMap,excMap,iInh_,iExc_,activation):
        self._data = excMap *  iExc_ - inhMap * iInh_



    def _onParamsUpdate(self,size,alpha,nspike,iExc,iInh,pExc,pInh):
        pExc_ = pExc**(1./(size))
        pInh_ = pInh**(1./(size))
        iExc_ = iExc/(size**2) * (40**2)/alpha * 1./nspike
        iInh_ = iInh/(size**2) * (40**2)/alpha * 1./nspike
        #print("pExc_ %s, pInh_ %s, iExc_ %s, iInh_ %s"%(pExc_,pInh_,iExc_,iInh_))

        return dict(pExc_=pExc_,pInh_=pInh_,iExc_=iExc_,iInh_=iInh_)

    def _childrenParamsUpdate(self,nspike,pInh_,pExc_):
        self.exc.setParams(nspike=nspike,proba=pExc_)
        self.inh.setParams(nspike=nspike,proba=pInh_)

    def _onAddChildren(self,**kwargs):
        if "activation" in kwargs.keys():
            actMap = kwargs.get("activation")
            self.exc.addChildren(activation=actMap)
            self.inh.addChildren(activation=actMap)
