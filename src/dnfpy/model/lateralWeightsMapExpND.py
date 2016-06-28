import dnfpy.core.utils as utils
import math
from dnfpy.core.funcMapND import FuncMap
from dnfpy.core.mapND import MapND
from dnfpy.model.lateralWeightsMapND import LateralWeightsMap

class LateralWeightsMapExp(LateralWeightsMap):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def initKernel(self,name,size,dim,dt,center,wrap,fashion):
        if fashion == 'chappet':
            kernFunc = utils.expNd
        elif fashion == 'fix':
            kernFunc = utils.expFix

        self.kernelExc = FuncMap(kernFunc,name+"_exc",size,dim,dt=dt,center=center,wrap=wrap,intensity=-1,proba=-1)
        self.kernelInh = FuncMap(kernFunc,name+"_inh",size,dim,dt=dt,center=center,wrap=wrap,intensity=-1,proba=-1)
        self.addChildren(exc=self.kernelExc,inh=self.kernelInh)

    @staticmethod
    def getScaledParams(size,globalSize,mapSize,alpha,iExc,iInh,wExc,wInh,dim):
        wExc_ = wExc**(1./globalSize)
        wInh_ = wInh**(1./globalSize)
        size = mapSize *  globalSize
        size = int(((math.floor(size/2.)) * 2) + 1)#Ensure odd
        iExc_ = iExc/(globalSize**dim) * (40**dim)/alpha
        iInh_ = iInh/(globalSize**dim) * (40**dim)/alpha

        return dict(size=size,wExc_=wExc_,wInh_=wInh_,iExc_=iExc_,iInh_=iInh_)

    def _onParamsUpdate(self,size,globalSize,mapSize,alpha,iExc,iInh,wExc,wInh,dim):
        return  LateralWeightsMapExp.getScaledParams(size,globalSize,mapSize,alpha,iExc,iInh,wExc,wInh,dim)
        

    def _childrenParamsUpdate(self,iExc_,iInh_,wExc_,wInh_):
        self.kernelExc.setParams(intensity=iExc_,proba=wExc_)
        self.kernelInh.setParams(intensity=iInh_,proba=wInh_)
        self.compute() #fix for the conf find something more elegant later
