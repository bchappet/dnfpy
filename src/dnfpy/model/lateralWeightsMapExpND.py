import dnfpy.core.utils as utils
import math
from dnfpy.core.funcMapND import FuncMap
from dnfpy.core.mapND import MapND
from dnfpy.model.lateralWeightsMapND import LateralWeightsMap

class LateralWeightsMapExp(LateralWeightsMap):

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)

        if fashion == 'chappet':
            kernFunc = utils.expNd
        elif fashion == 'fix':
            kernFunc = utils.expFix

        self.kernelExc = FuncMap(kernFunc,name+"_exc",self.size,self.dim,dt=dt,center=self.center,wrap=wrap,intensity=iExc,proba=wExc)
        self.kernelInh = FuncMap(kernFunc,name+"_inh",self.size,self.dim,dt=dt,center=self.center,wrap=wrap,intensity=iInh,proba=wInh)
        self.addChildren(exc=self.kernelExc,inh=self.kernelInh)

    @staticmethod
    def getScaledParams(size,globalSize,mapSize,alpha,iExc,iInh,pExc,pInh,dim):
        pExc_ = pExc**(1./globalSize)
        pInh_ = pInh**(1./globalSize)
        size = mapSize *  globalSize
        size = int(((math.floor(size/2.)) * 2) + 1)#Ensure odd
        iExc_ = iExc/(globalSize**dim) * (40**dim)/alpha
        iInh_ = iInh/(globalSize**dim) * (40**dim)/alpha

        return dict(size=size,pExc_=pExc_,pInh_=pInh_,iExc_=iExc_,iInh_=iInh_)

    def _onParamsUpdate(self,size,globalSize,mapSize,alpha,iExc,iInh,pExc,pInh,dim):
        return  LateralWeightsMapExpND.getScaledParams(size,globalSize,mapSize,alpha,iExc,iInh,pExc,pInh,dim)
        

    def _childrenParamsUpdate(self,iExc_,iInh_,pExc_,pInh_):
        self.kernelExc.setParams(intensity=iExc_,proba=pExc_)
        self.kernelInh.setParams(intensity=iInh_,proba=pInh_)
        self.compute() #fix for the conf find something more elegant later
