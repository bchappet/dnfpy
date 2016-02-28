from dnfpy.cellular.nSpikeMap import NSpikeMap
from dnfpy.cellular.rsdnfMap import RsdnfMap
import numpy as np
from dnfpy.core.map2D import Map2D


class RsdnfConvolution(NSpikeMap):
    """
    Children needed: "activation" with map of 0 and 1 of type np.intc
    """
    def __init__(self,name,size,dt=0.1,nspike=20,
                 iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.4,alpha=10,
                 iExc_=1.,iInh_=1.,pInh_=0.,pExc_=0.,
                 reproductible=True,
                 **kwargs):
        super(RsdnfConvolution,self).__init__(name,size,dt=dt,nspike=nspike,
                iExc=iExc,iInh=iInh,pExc=pExc,pInh=pInh,alpha=alpha,
                 iExc_=iExc_,iInh_=iInh_,pInh_=pInh_,pExc_=pExc_,
                reproductible=reproductible,
                                               **kwargs)
        self.inh = RsdnfMap(name+"_inh",size,dt=dt,nspike=nspike,
                             proba=pInh_,reproductible=reproductible)
        self.exc = RsdnfMap(name+"_exc",size,dt=dt,nspike=nspike,
                             proba=pExc_,reproductible=reproductible)

        self.addChildren(inhMap = self.inh,excMap = self.exc)
