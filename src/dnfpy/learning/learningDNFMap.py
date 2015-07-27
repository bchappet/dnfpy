from dnfpy.core.map2D import Map2D
import numpy as np
from dnfpy.model.activationMap import ActivationMap
from greedyConvolution import GreedyConvolution
from learningMap import STDPLearningMap


class LearningDNFMap(Map2D):
    def __init__(self,name,size,dt,sizeKernel,tau=0.64,h=0,th=0.75,**kwargs):
        super(LearningDNFMap,self).__init__(name=name,size=size,dt=dt,sizeKernel=sizeKernel,
                                            tau=tau,h=h,
                                            th= th,**kwargs)
        self.lateralWeights = STDPLearningMap("latW",size,dt,sizeKernel=sizeKernel)
        self.lat = GreedyConvolution("conv",size,dt) #"convolution" of activation per lateralWeights
        self.activation = ActivationMap("act",size,dt,model="spike",th=th)

        self.activation.addChildren(field=self)
        self.addChildren(lat=self.lat)
        self.lat.addChildren(source=self.activation,lateralWeights=self.lateralWeights)
        self.lateralWeights.addChildren(source=self.activation)


    def getActivation(self):
        return self.activation

    def getArrays(self):
        return [self.activation,self.lat,self.lateralWeights]




    def _compute(self,lat,aff,dt,tau,h,th):
        self._data = np.where(self._data > th,0.,self._data) # if x > th => x = 0
        self._data = self._data + dt/tau*(-self._data + h + aff ) +  1/tau*lat



