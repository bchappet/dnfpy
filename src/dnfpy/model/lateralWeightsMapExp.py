import dnfpy.core.utils as utils
from dnfpy.core.funcMap2D import FuncMap2D

class LateralWeightsMapExp(FuncMap2D):

    def __init__(self,size,dt,wrap,iExc,iInh,pExc,pInh,**kwargs):
        super(LateralWeightsMapExp,self).__init__(utils.subArrays,size,*kwargs)
        center = (size - 1)/2
        self.kernelExc = FuncMap2D(utils.exp2d,size,dt=dt,centerX=center,
                              centerY=center,wrap=wrap,intensity=iExc,proba=pExc)
        self.kernelInh = FuncMap2D(utils.exp2d,size,dt=dt,centerX=center,
                              centerY=center,wrap=wrap,intensity=iInh,proba=pInh)
        self.addChildren(a=self.kernelExc,b=self.kernelInh)

    def _onParamsUpdate(self,globalSize,alpha,iExc,iInh,pExc,pInh):
        pExc = pExc**(1./globalSize)
        pInh = pInh**(1./globalSize)
        iExc = iExc/(globalSize**2) * (40**2)/alpha
        iInh = iInh/(globalSize**2) * (40**2)/alpha
        #TODO find a way to do it automatically
        self.kernelExc.setArg(iExc=iExc,pExc=pExc)
        self.kernelInh.setArg(iInh=iInh,pInh=pInh)



        return dict(pExc=pExc,pInh=pInh,iExc=iExc,iInh=iInh)
