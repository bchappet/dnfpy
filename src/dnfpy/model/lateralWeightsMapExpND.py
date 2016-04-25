import dnfpy.core.utilsND as utils
import math
from dnfpy.core.funcMapND import FuncMapND
from dnfpy.core.mapND import MapND

class LateralWeightsMapExpND(MapND):

    def __init__(self,name,globalSize,dim=1,mapSize=1,dt=1e10,wrap=True,
                 iExc=1.25,iInh=0.7,pExc=0.1,pInh=10,alpha=10.0,
                pExc_=1,pInh_=1,iExc_=1,iInh_=1,nbStep=0,fashion='chappet',**kwargs):
        super().__init__(
            name=name,size=globalSize,globalSize=globalSize,
            mapSize = mapSize,nbStep=nbStep,dim=dim,
            dt=dt,wrap=wrap,
            iExc_=iExc_,iInh_=iInh_,pExc_=pExc_,pInh_=pInh_,
            pExc=pExc, pInh=pInh,iExc=iExc,iInh=iInh,alpha=alpha,
            fashion=fashion,**kwargs)

        size = self.getArg('size')
        dim = self.getArg('dim')
        center = ((size//2),)*dim

        if fashion == 'chappet':
            kernFunc = utils.expNd
        elif fashion == 'fix':
            kernFunc = utils.expFix

        self.kernelExc = FuncMapND(kernFunc,name+"_exc",size,dim,dt=dt,center=center,wrap=wrap,intensity=iExc,proba=pExc)
        self.kernelInh = FuncMapND(kernFunc,name+"_inh",size,dim,dt=dt,center=center,wrap=wrap,intensity=iInh,proba=pInh)
        self.addChildren(exc=self.kernelExc,inh=self.kernelInh)

    def _compute(self,exc,inh,nbStep):
        ret = exc - inh
        if nbStep > 0:
            ret = utils.discretize(ret,nbStep=nbStep)
        else:
            pass
        self._data = ret

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
