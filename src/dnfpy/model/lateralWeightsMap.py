import dnfpy.core.utils as utils
import math
from dnfpy.core.funcMap2D import FuncMap2D

class LateralWeightsMap(FuncMap2D):

    def __init__(self,name,globalSize,mapSize=1,dt=1e10,wrap=True,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10,alpha=10,**kwargs):
        super(LateralWeightsMap,self).__init__(
            utils.subArrays,name,size=globalSize,globalSize=globalSize,
            mapSize = mapSize,
            dt=dt,wrap=wrap,iExc=iExc,
            iInh=iInh,wExc=wExc,wInh=wInh,alpha=alpha,**kwargs)
        size = self.getArg('size')
        center = (size - 1)/2
        self.kernelExc = FuncMap2D(utils.gauss2d,name+"_exc",size,dt=dt,centerX=center,
                              centerY=center,wrap=wrap,intensity=iExc,width=wExc)
        self.kernelInh = FuncMap2D(utils.gauss2d,name+"_inh",size,dt=dt,centerX=center,
                              centerY=center,wrap=wrap,intensity=iInh,width=wInh)
        self.addChildren(a=self.kernelExc,b=self.kernelInh)

    def _onParamsUpdate(self,size,globalSize,mapSize,alpha,iExc,iInh,wExc,wInh):
        wExc = wExc*globalSize
        wInh = wInh*globalSize
        size = mapSize *  globalSize
        size = int(((math.floor(size/2.)) * 2) + 1)#Ensure odd
        iExc = iExc/(globalSize**2) * (40**2)/alpha
        iInh = iInh/(globalSize**2) * (40**2)/alpha

        return dict(size=size,wExc=wExc,wInh=wInh,iExc=iExc,iInh=iInh)

    def _childrenParamsUpdate(self,iExc,iInh,wExc,wInh):
        self.kernelExc.setParams(intensity=iExc,width=wExc)
        self.kernelInh.setParams(intensity=iInh,width=wInh)
