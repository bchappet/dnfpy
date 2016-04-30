import dnfpy.core.utils as utils
import math
from dnfpy.core.map2D import Map2D
import numpy as np
from dnfpy.core.funcMap2D import FuncMap2D
from dnfpy.model.lateralWeightsMapND import LateralWeightsMap


class LateralWeightsMapLin(LateralWeightsMap):
    """
    Map describing the lateral weights of the dynamic neural fields
    The lateral weights are usually a sum of excitatory and inhibitory weights
    In this case the lateral weights is a difference of Linear functions (triangles)
    alpha : slope of the triangle
    beta : top of the triangle


    ex python main.py ModelDNF 51 1 "{'lateral':'dol','wExc':0.4,'iExc':1.4,'wInh':0.01,'iInh':0.8}"

    """
    def __init__(self,name,globalSize,mapSize=1,dt=1e10,wrap=True,
                 betaExc=1.25,betaInh=0.7,alphaExc=0.1,alphaInh=10,alpha=10,
                 alphaExc_=1,alphaInh_=1,betaExc_=1,betaInh_=1,nbStep=0.0,
                 **kwargs):
        super().__init__(
            name=name,size=globalSize,globalSize=globalSize,
            mapSize = mapSize,nbStep=nbStep,
            dt=dt,wrap=wrap,
            betaExc_=betaExc_,betaInh_=betaInh_,alphaExc_=alphaExc_,alphaInh_=alphaInh_,
            alphaExc=alphaExc, alphaInh=alphaInh,betaExc=betaExc,betaInh=betaInh,alpha=alpha,**kwargs)
        size = self.getArg('size')
        center = (size - 1)/2

        self.kernelExc = FuncMap2D(utils.lin2d,name+"_exc",size,dt=dt,centerX=center,
                              centerY=center,wrap=wrap,alpha=alphaExc_,beta=betaExc_)
        self.kernelInh = FuncMap2D(utils.lin2d,name+"_inh",size,dt=dt,centerX=center,
                              centerY=center,wrap=wrap,alpha=alphaInh_,beta=betaInh_)
        self.addChildren(exc=self.kernelExc,inh=self.kernelInh)

    @staticmethod
    def getScaledParams(size,globalSize,mapSize,alpha,alphaExc,alphaInh,betaExc,betaInh):
        alphaExc_ = alphaExc/globalSize
        alphaInh_ = alphaInh/globalSize
        size = mapSize *  globalSize
        size = int(((math.floor(size/2.)) * 2) + 1)#Ensure odd
        betaExc_ = betaExc/(globalSize) * (40**2)/alpha
        betaInh_ = betaInh/(globalSize) * (40**2)/alpha

        return dict(size=size,alphaExc_=alphaExc_,alphaInh_=alphaInh_,betaExc_=betaExc_,betaInh_=betaInh_)

    def _onParamsUpdate(self,size,globalSize,mapSize,alpha,alphaExc,alphaInh,betaExc,betaInh):
        return getScaledParams(size,globalSize,mapSize,alpha,alphaExc,alphaInh,betaExc,betaInh)

    def _childrenParamsUpdate(self,betaExc_,betaInh_,alphaExc_,alphaInh_):
        self.kernelExc.setParams(alpha=alphaExc_,beta=betaExc_)
        self.kernelInh.setParams(alpha=alphaInh_,beta=betaInh_)
        self.compute() #fix for the conf find something more elegant later
