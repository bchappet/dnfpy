import dnfpy.core.utils as utils
from dnfpy.core.funcMap2D import FuncMap2D

class LateralWeightsMap(FuncMap2D):

    def __init__(self,size,globalSize,dt=0.1,wrap=True,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10,alpha=10,**kwargs):
        super(LateralWeightsMap,self).__init__(
            utils.subArrays,size,globalSize=globalSize,dt=dt,wrap=wrap,iExc=iExc,
            iInh=iInh,wExc=wExc,wInh=wInh,alpha=alpha,**kwargs)
        center = (size - 1)/2
        self.kernelExc = FuncMap2D(utils.gauss2d,size,dt=dt,centerX=center,
                              centerY=center,wrap=wrap,intensity=iExc,width=wExc)
        self.kernelInh = FuncMap2D(utils.gauss2d,size,dt=dt,centerX=center,
                              centerY=center,wrap=wrap,intensity=iInh,width=wInh)
        self.addChildren(a=self.kernelExc,b=self.kernelInh)

    def _onParamsUpdate(self,globalSize,alpha,iExc,iInh,wExc,wInh):
        wExc = wExc*globalSize
        wInh = wInh*globalSize
        iExc = iExc/(globalSize**2) * (40**2)/alpha
        iInh = iInh/(globalSize**2) * (40**2)/alpha
        return dict(wExc=wExc,wInh=wInh,iExc=iExc,iInh=iInh)

    def _childrenParamsUpdate(self,iExc,iInh,wExc,wInh):
        self.kernelExc.setArg(intensity=iExc,width=wExc)
        self.kernelInh.setArg(intensity=iInh,width=wInh)
