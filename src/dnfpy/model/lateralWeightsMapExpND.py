import dnfpy.core.utils as utils
import math
from dnfpy.core.funcMap2D import FuncMap2D
from dnfpy.core.map2D import Map2D

class LateralWeightsMapExpND(Map2D):

    def __init__(self,name,globalSize,mapSize=1,dt=1e10,wrap=True,
                 iExc=1.25,iInh=0.7,pExc=0.1,pInh=10,alpha=10.0,
                pExc_=1,pInh_=1,iExc_=1,iInh_=1,nbStep=0,
                 **kwargs):
        super(LateralWeightsMapExp,self).__init__(
            name=name,size=globalSize,globalSize=globalSize,
            mapSize = mapSize,nbStep=nbStep,
            dt=dt,wrap=wrap,
            iExc_=iExc_,iInh_=iInh_,pExc_=pExc_,pInh_=pInh_,
            pExc=pExc, pInh=pInh,iExc=iExc,iInh=iInh,alpha=alpha,
            **kwargs)
        size = self.getArg('size')
        center = (size - 1)/2

        self.kernelExc = FuncMap2D(utils.exp2d,name+"_exc",size,dt=dt,centerX=center,
                              centerY=center,wrap=wrap,intensity=iExc,proba=pExc)
        self.kernelInh = FuncMap2D(utils.exp2d,name+"_inh",size,dt=dt,centerX=center,
                              centerY=center,wrap=wrap,intensity=iInh,proba=pInh)
        self.addChildren(exc=self.kernelExc,inh=self.kernelInh)

    def _compute(self,exc,inh,nbStep):
        ret = exc - inh
        if nbStep > 0:
            ret = utils.discretize(ret,nbStep=nbStep)
        else:
            pass
        self._data = ret

    @staticmethod
    def getScaledParams(size,globalSize,mapSize,alpha,iExc,iInh,pExc,pInh):
        pExc_ = pExc**(1./globalSize)
        pInh_ = pInh**(1./globalSize)
        size = mapSize *  globalSize
        size = int(((math.floor(size/2.)) * 2) + 1)#Ensure odd
        iExc_ = iExc/(globalSize) * (40**2)/alpha
        iInh_ = iInh/(globalSize) * (40**2)/alpha

        return dict(size=size,pExc_=pExc_,pInh_=pInh_,iExc_=iExc_,iInh_=iInh_)

    def _onParamsUpdate(self,size,globalSize,mapSize,alpha,iExc,iInh,pExc,pInh):
        return  getScaledParams(size,globalSize,mapSize,alpha,iExc,iInh,pExc,pInh)
        

    def _childrenParamsUpdate(self,iExc_,iInh_,pExc_,pInh_):
        self.kernelExc.setParams(intensity=iExc_,proba=pExc_)
        self.kernelInh.setParams(intensity=iInh_,proba=pInh_)
        self.compute() #fix for the conf find something more elegant later
