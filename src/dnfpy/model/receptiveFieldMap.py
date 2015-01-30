from lateralWeightsMap import LateralWeightsMap
from dnfpy.model.convolution import Convolution


class ReceptiveFieldMap(Convolution):
    def __init__(self,name,size,dt=0.1,wrap=True,mapSize=1.,
                 intensity = 1.,width=0.1,alpha=10.0,nbStep=0):
        super(ReceptiveFieldMap,self).__init__(name,size=size,dt=dt,wrap=wrap)

        self.kernel = LateralWeightsMap(name+"_kernel",mapSize=mapSize,
                                        globalSize=size,wrap=wrap,iExc=intensity,
                                        iInh=0.,wExc=width,wInh=1.,alpha=alpha,nbStep=nbStep)

        self.addChildren(kernel=self.kernel)

