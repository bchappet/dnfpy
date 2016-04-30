import dnfpy.core.utilsND as utils
import math
from dnfpy.core.mapND import MapND
import numpy as np
from dnfpy.core.funcMapND import FuncMapND


class LateralWeightsMap(MapND):
    """
    Map describing the lateral weights of the dynamic neural fields
    The lateral weights are usually a sum of excitatory and inhibitory weights
    In this case the lateral weights is a difference of Gaussiana

    fashion : string \in {chappet,fix} change the way of computing lateral kernel (refer to dnfpy.core.utils to see the functions)

    """
    def __init__(self,name,globalSize,dim=1,mapSize=1,dt=1e10,wrap=True,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=1,alpha=10,
                wExc_=1,wInh_=1,iExc_=1,iInh_=1,nbStep=0,
                fashion='chappet',
                 **kwargs):
        super().__init__(
            name=name,size=globalSize,dim=dim,globalSize=globalSize,
            mapSize = mapSize,nbStep=nbStep,
            dt=dt,wrap=wrap,iExc=iExc,
            wExc_=wExc_,wInh_=wInh_,iExc_=iExc_,iInh_=iInh_,
            iInh=iInh,wExc=wExc,wInh=wInh,alpha=alpha,**kwargs)

        size = self.getArg('size')
        dim = self.getArg('dim')
        self.center = ((size//2),)*dim
        self.initKernel(name,size,dim,dt,self.center,wrap,fashion)

    def initKernel(self,name,size,dim,dt,center,wrap,fashion):
        if fashion == 'chappet':
            kernFunc = utils.gaussNd
        elif fashion == 'fix':
            kernFunc = utils.gaussFix

        self.kernelExc = FuncMapND(kernFunc,name+"_exc",size,dim=dim,dt=dt,center=center,
                              wrap=wrap,intensity=iExc_,width=wExc_)
        self.kernelInh = FuncMapND(kernFunc,name+"_inh",size,dim=dim,dt=dt,center=center,
                              wrap=wrap,intensity=iInh_,width=wInh_)
        self.addChildren(exc=self.kernelExc,inh=self.kernelInh)

    def _compute(self,exc,inh,nbStep,size,dim):
        ret = exc - inh
        if nbStep > 0:
            ret = utils.discretize(ret,nbStep=nbStep)
        else:
            pass
        #ensure that there is no self activation?? 
        ret[self.center] = 0
        self._data = ret

    @staticmethod
    def getScaledParams(size,globalSize,mapSize,dim,alpha,iExc,iInh,wExc,wInh):
        wExc_ = (wExc*globalSize)
        wInh_ = (wInh*globalSize)
        size = mapSize *  globalSize
        size = int(((math.floor(size/2.)) * 2) + 1)#Ensure odd
        iExc_ = iExc/(globalSize**dim) * (40**dim)/alpha
        iInh_ = iInh/(globalSize**dim) * (40**dim)/alpha
        #print(size,globalSize,mapSize,dim,alpha,iExc,iInh,wExc,wInh)

        #print(iExc_,iInh_,wExc_,wInh_)

        return dict(size=size,wExc_=wExc_,wInh_=wInh_,iExc_=iExc_,iInh_=iInh_)


    def _onParamsUpdate(self,size,globalSize,mapSize,dim,alpha,iExc,iInh,wExc,wInh):
        return LateralWeightsMapND.getScaledParams(size,globalSize,mapSize,dim,alpha,iExc,iInh,wExc,wInh)


    def _childrenParamsUpdate(self,iExc_,iInh_,wExc_,wInh_):
        self.kernelExc.setParams(intensity=iExc_,width=wExc_)
        self.kernelInh.setParams(intensity=iInh_,width=wInh_)
        self.compute() #fix for the conf find something more elegant later
