import dnfpy.core.utils as utils
import math
from dnfpy.core.mapND import MapND
import numpy as np
from dnfpy.core.funcMapND import FuncMap
from dnfpy.model.lateralWeightsMapND import LateralWeightsMap


class LateralWeightsMapStep(LateralWeightsMap):
    """
    Map describing the lateral weights of the dynamic neural fields
    The lateral weights are usually a sum of excitatory and inhibitory weights
    In this case the lateral weights is a difference of Gaussiana

    fashion : string \in {chappet,fix} change the way of computing lateral kernel (refer to dnfpy.core.utils to see the functions)

    """

    def initKernel(self,name,size,dim,dt,center,wrap,fashion):
        if fashion == 'chappet':
            kernFunc = utils.stepNd
        elif fashion == 'fix':
            kernFunc = utils.stepFix #TODO

        self.kernelExc = FuncMap(kernFunc,name+"_exc",size,dim=dim,dt=dt,center=center,
                              wrap=wrap,intensity=-1,width=-1)
        self.kernelInh = FuncMap(kernFunc,name+"_inh",size,dim=dim,dt=dt,center=center,
                              wrap=wrap,intensity=-1,width=-1)
        self.addChildren(exc=self.kernelExc,inh=self.kernelInh)

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
        return LateralWeightsMapStep.getScaledParams(size,globalSize,mapSize,dim,alpha,iExc,iInh,wExc,wInh)


    def _childrenParamsUpdate(self,iExc_,iInh_,wExc_,wInh_):
        self.kernelExc.setParams(intensity=iExc_,width=wExc_)
        self.kernelInh.setParams(intensity=iInh_,width=wInh_)
        self.compute() #fix for the conf find something more elegant later
