import dnfpy.core.utilsND as utils
import math
from dnfpy.core.mapSpace import MapSpace
import numpy as np
from dnfpy.core.funcMapSpace import FuncMapSpace


class LateralWeightsMapSpace(MapSpace):
    """

    """
    def __init__(self,name,space,dt=1e10,wrap=True,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=1,
                iExc_=1,iInh_=1,nbStep=0,
                fashion='chappet',lateral='dog',
                globalInh=0.0,
                 **kwargs):
        super().__init__(
            name=name,space=space,nbStep=nbStep,
            dt=dt,wrap=wrap,iExc=iExc,
            iExc_=iExc_,iInh_=iInh_,
            iInh=iInh,wExc=wExc,wInh=wInh,
            globalInh=globalInh,
            **kwargs)


        


        

        if fashion == 'fix':
            self.kernelExc = FuncMapSpace(utils.weightsFix,name+"_exc",space,dt=dt,lat=lateral,k=iExc_,w=wExc)
            self.kernelInh = FuncMapSpace(utils.weightsFix,name+"_inh",space,dt=dt,lat=lateral,k=iInh_,w=wInh)
        else:
            print("fashion: " + fashion + " is not available in this class: " + self)

        self.addChildren(exc=self.kernelExc,inh=self.kernelInh)

    def _compute(self,exc,inh,nbStep,globalInh,space):
        ret = exc - inh - globalInh
        if nbStep > 0:
            ret = utils.discretize(ret,nbStep=nbStep)
        else:
            pass
        #ensure that theris no self activation?? 
        #ret[center] = 0
        self._data = ret

    def _onParamsUpdate(self,dx,dim,iExc,iInh):
        return LateralWeightsMapSpace.getScaledParams(dx,dim,iExc,iInh)

    @staticmethod
    def getScaledParams(dx,dim,iExc,iInh):
        #The convolution needs to be normalized
        iExc_ = iExc*dx**dim
        iInh_ = iInh*dx**dim
        #print("iExc _ :", iExc_, "iInh_ : ",iInh_)
        return dict(iExc_=iExc_,iInh_=iInh_)

    def _childrenParamsUpdate(self,iExc_,iInh_):
        self.kernelExc.setParams(k=iExc_)
        self.kernelInh.setParams(k=iInh_)
        self.compute() #fix for the conf find something more elegant later




