import dnfpy.core.utils as utils
import math
from dnfpy.core.map2D import Map2D
import numpy as np
from dnfpy.core.funcMap2D import FuncMap2D




class LateralWeightsMap(Map2D):
    """
    Map describing the lateral weights of the dynamic neural fields
    The lateral weights are usually a sum of excitatory and inhibitory weights
    In this case the lateral weights is a difference of Gaussian

    """
    def __init__(self,name,globalSize,mapSize=1,dt=1e10,wrap=True,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10,alpha=10,
                wExc_=1,wInh_=1,iExc_=1,iInh_=1,nbStep=0,
                 **kwargs):
        super(LateralWeightsMap,self).__init__(
            name=name,size=globalSize,globalSize=globalSize,
            mapSize = mapSize,nbStep=nbStep,
            dt=dt,wrap=wrap,iExc=iExc,
            wExc_=wExc_,wInh_=wInh_,iExc_=iExc_,iInh_=iInh_,
            iInh=iInh,wExc=wExc,wInh=wInh,alpha=alpha,**kwargs)
        size = self.getArg('size')
        center = (size - 1)/2

        self.kernelExc = FuncMap2D(utils.gauss2d,name+"_exc",size,dt=dt,centerX=center,
                              centerY=center,wrap=wrap,intensity=iExc_,width=wExc_)
        self.kernelInh = FuncMap2D(utils.gauss2d,name+"_inh",size,dt=dt,centerX=center,
                              centerY=center,wrap=wrap,intensity=iInh_,width=wInh_)
        self.addChildren(exc=self.kernelExc,inh=self.kernelInh)

    def _compute(self,exc,inh,nbStep):
        ret = exc - inh
        if nbStep > 0:
            ret = utils.discretize(ret,nbStep=nbStep)
        else:
            pass
        self._data = ret

    @staticmethod
    def getScaledParams(size,globalSize,mapSize,alpha,iExc,iInh,wExc,wInh):
        wExc_ = wExc*globalSize
        wInh_ = wInh*globalSize
        size = mapSize *  globalSize
        size = int(((math.floor(size/2.)) * 2) + 1)#Ensure odd
        iExc_ = iExc/(globalSize**2) * (40**2)/alpha
        iInh_ = iInh/(globalSize**2) * (40**2)/alpha
        #print("globalSize",globalSize)
        #print(iExc_,iInh_,wExc_,wInh_)

        return dict(size=size,wExc_=wExc_,wInh_=wInh_,iExc_=iExc_,iInh_=iInh_)


    def _onParamsUpdate(self,size,globalSize,mapSize,alpha,iExc,iInh,wExc,wInh):
        return LateralWeightsMap.getScaledParams(size,globalSize,mapSize,alpha,iExc,iInh,wExc,wInh)


    def _childrenParamsUpdate(self,iExc_,iInh_,wExc_,wInh_):
        self.kernelExc.setParams(intensity=iExc_,width=wExc_)
        self.kernelInh.setParams(intensity=iInh_,width=wInh_)
        self.compute() #fix for the conf find something more elegant later
