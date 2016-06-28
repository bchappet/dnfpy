import numpy as np
from dnfpy.model.convolutionND import ConvolutionND
from dnfpy.model.lateralWeightsMapND import LateralWeightsMap
from dnfpy.model.lateralWeightsMapExpND import LateralWeightsMapExp
from dnfpy.model.lateralWeightsMapLinND import LateralWeightsMapLin
from dnfpy.model.lateralWeightsMapStep import LateralWeightsMapStep
from dnfpy.core.constantMapND import ConstantMap

class KernelConvolution(ConvolutionND):
    """
    Afferent map with a single kernel (gaussian by default)
    """
    def __init__(self,name,size,dim=1,dt=0.1,lateral='dog',wExc=0.0,iExc=0.0,wInh=0.0,iInh=0.0,wrap=True,
            alpha=10.0,fashion="chappet",nbStep=0,value=np.zeros((0)),
            **kwargs):
        super().__init__(name,size,dim=dim,dt=dt,lateral=lateral,wrap=wrap,
                **kwargs)

        mapSize = 2.0 if not(wrap) else 1.0
        globalSize = size
        if lateral=='dog':
            self.kernel = LateralWeightsMap("Kernel"+name,mapSize=mapSize,dim=dim,
                                        globalSize=globalSize,wrap=wrap,
                                        iExc=iExc,iInh=iInh,wExc=wExc,
                                        wInh=wInh,alpha=alpha,nbStep=nbStep,fashion=fashion)
        elif lateral=='doe':
            self.kernel = LateralWeightsMapExp("Kernel"+name,mapSize=mapSize,dim=dim,
                                        globalSize=globalSize,wrap=wrap,
                                        iExc=iExc,iInh=iInh,wExc=wExc,
                                        wInh=wInh,alpha=alpha,nbStep=nbStep,fashion=fashion)
        elif lateral=='dol':
            self.kernel = LateralWeightsMapLin("Kernel"+name,mapSize=mapSize,dim=dim,
                                        globalSize=globalSize,wrap=wrap,
                                        betaExc=iExc,betaInh=iInh,alphaExc=wExc,
                                        alphaInh=wInh,alpha=alpha,nbStep=nbStep,fashion=fashion)
        elif lateral=='step':
            self.kernel = LateralWeightsMapStep("Kernel"+name,mapSize=mapSize,dim=dim,
                                        globalSize=globalSize,wrap=wrap,iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh)
        elif lateral=='constant':
            self.kernel = ConstantMap("Kernel"+name,size=size,value=value)
        else:
            raise("Parameter lateral should be 'dog', 'doe' or 'dol'. %s invalid"%(lateral))

        self.addChildren(kernel=self.kernel)
