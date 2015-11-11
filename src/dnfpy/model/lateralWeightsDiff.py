import dnfpy.core.utils as utils
import math
from dnfpy.core.mapND import MapND
from dnfpy.core.funcMapND import FuncMapND
from dnfpy.cellular.diffusionMap import DiffusionMap
import numpy as np




class LateralWeightsDiff(MapND):
    """
    Map describing the lateral weights of the dynamic neural fields
    The lateral weights are usually a sum of excitatory and inhibitory weights
    In this case the lateral weights is a difference of Gaussian

    """
    def __init__(self,name,size,dim,dt=0.1,wrap=True,
                    wExc=0.5,wInh=2.0,iExc=0.6,iInh=1.0,
                    wExc_=1.0,wInh_=1.0,iExc_=1.0,iInh_=1.0,
                    leakE=0.11,leakI=0.01,
                 **kwargs):
        super().__init__(
            name,size,dim,dt=dt,wrap=wrap,
            wExc=wExc,wInh=wInh,iExc=iExc,iInh=iInh,
            wExc_=wExc_,wInh_=wInh_,iExc_=iExc_,iInh_=iInh_,
            **kwargs)
        
        size = self.getArg('size')
        center = (size - 1)/2

        self.kernelExc = DiffusionMap(name+"_exc",size,dim=dim,dt=dt,wrap=wrap,D=wExc_,leak=leakE)
        self.kernelInh = DiffusionMap(name+"_inh",size,dim=dim,dt=dt,wrap=wrap,D=wInh_,leak=leakI)
        self.addChildren(exc=self.kernelExc,inh=self.kernelInh)

    def _compute(self,exc,inh,iExc_,iInh_):
        lat = iExc_*exc - iInh_*inh
        self._data = lat

    @staticmethod
    def getScaledParams(size,iExc,iInh,wExc,wInh):
        size = int(((math.floor(size/2.)) * 2) + 1)#Ensure odd
        wExc_ = wExc
        wInh_ = wInh
        iExc_ = iExc
        iInh_ = iInh
        #print("globalSize",globalSize)
        #print(iExc_,iInh_,wExc_,wInh_)

        return dict(size=size,wExc_=wExc_,wInh_=wInh_,iExc_=iExc_,iInh_=iInh_)

    def _onParamsUpdate(self,size,iExc,iInh,wExc,wInh):
        return self.getScaledParams(size,iExc,iInh,wExc,wInh)

    def _onAddChildren(self,**kwargs):
        if "act" in kwargs.keys():
            self.kernelExc.addChildren(act=kwargs['act'])
            self.kernelInh.addChildren(act=kwargs['act'])


    def _childrenParamsUpdate(self,wExc_,wInh_):
        self.kernelExc.setParams(D=wExc_)
        self.kernelInh.setParams(D=wInh_)
