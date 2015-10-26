import dnfpy.core.utilsND as utils
import math
from dnfpy.core.mapND import MapND
import numpy as np
from dnfpy.core.funcMapND import FuncMapND


class LateralWeightsMapND(MapND):
    """
    Map describing the lateral weights of the dynamic neural fields
    The lateral weights are usually a sum of excitatory and inhibitory weights
    In this case the lateral weights is a difference of Gaussiana

    """
    def __init__(self,name,globalSize,mapSize=1,dt=1e10,wrap=True,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=1,alpha=10,
                wExc_=1,wInh_=1,iExc_=1,iInh_=1,nbStep=0,
                 **kwargs):
        super(LateralWeightsMapND,self).__init__(
            name=name,size=globalSize,globalSize=globalSize,
            mapSize = mapSize,nbStep=nbStep,
            dt=dt,wrap=wrap,iExc=iExc,
            wExc_=wExc_,wInh_=wInh_,iExc_=iExc_,iInh_=iInh_,
            iInh=iInh,wExc=wExc,wInh=wInh,alpha=alpha,**kwargs)
        size = self.getArg('size')
        center = (size - 1)/2

        self.kernelExc = FuncMapND(utils.gaussNd,name+"_exc",size,dt=dt,center=center,
                              wrap=wrap,intensity=iExc_,width=wExc_)
        self.kernelInh = FuncMapND(utils.gaussNd,name+"_inh",size,dt=dt,center=center,
                              wrap=wrap,intensity=iInh_,width=wInh_)
        self.addChildren(exc=self.kernelExc,inh=self.kernelInh)

    def _compute(self,exc,inh,nbStep,size):
        center = (size - 1)/2
        ret = exc - inh
        if nbStep > 0:
            ret = utils.discretize(ret,nbStep=nbStep)
        else:
            pass
        #ensure that theris no self activation?? 
        #ret[center] = 0
        self._data = ret

    @staticmethod
    def getScaledParams(size,globalSize,mapSize,alpha,iExc,iInh,wExc,wInh):
        wExc_ = wExc*globalSize
        wInh_ = wInh*globalSize
        size = mapSize *  globalSize
        size = int(((math.floor(size/2.)) * 2) + 1)#Ensure odd
        iExc_ = iExc/(globalSize) * (40**2)/alpha
        iInh_ = iInh/(globalSize) * (40**2)/alpha
        print(iExc_,iInh_,wExc_,wInh_)

        return dict(size=size,wExc_=wExc_,wInh_=wInh_,iExc_=iExc_,iInh_=iInh_)


    def _onParamsUpdate(self,size,globalSize,mapSize,alpha,iExc,iInh,wExc,wInh):
        return LateralWeightsMap.getScaledParams(self,size,globalSize,mapSize,alpha,iExc,iInh,wExc,wInh)


    def _onParamsUpdate(self,size,globalSize,mapSize,alpha,iExc,iInh,wExc,wInh):
        wExc_ = wExc*globalSize
        wInh_ = wInh*globalSize
        size = mapSize *  globalSize
        size = int(((math.floor(size/2.)) * 2) + 1)#Ensure odd
        iExc_ = iExc/(globalSize) * (60)/alpha
        iInh_ = iInh/(globalSize) * (60)/alpha
        print("globalSize",globalSize)
        print(iExc_,iInh_,wExc_,wInh_)
        #print("iExc_",iExc_)
        #print("iInh_",iInh_)
        #print("WExc_",wExc_)
        #print("WInh_",wInh_)

        return dict(size=size,wExc_=wExc_,wInh_=wInh_,iExc_=iExc_,iInh_=iInh_)

    def _childrenParamsUpdate(self,iExc_,iInh_,wExc_,wInh_):
        self.kernelExc.setParams(intensity=iExc_,width=wExc_)
        self.kernelInh.setParams(intensity=iInh_,width=wInh_)
        self.compute() #fix for the conf find something more elegant later
