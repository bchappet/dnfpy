from dnfpy.core.map2D import Map2D
from dnfpy.model.noiseMap import NoiseMap
import numpy as np

class FieldMap(Map2D):
    def __init__(self,name,size,dt=0.1,model='cnft',tau=0.64,h=0,th=0.75,delta=1.,
                    resetLat=False,noiseI=0.0,
                    **kwargs):
        super(FieldMap,self).__init__(name,size,dt=dt,model=model,
                                      tau=tau,h=h,th=th,delta=delta,
                                      resetLat=resetLat,noiseI=noiseI,
                                      **kwargs)
        self.noise = NoiseMap(name+"_noise",size=size,dt=dt,intensity=noiseI)
        self.addChildren(noise=self.noise)

    def _compute(self,model,lat,aff,dt,tau,h,th,delta,resetLat,noise):

        if model == 'cnft':
            self._data = self._data + dt/tau*(-self._data + h + aff + delta*lat) + noise
        elif model == 'spike':
            self._data = np.where(self._data > th,0.,self._data) # if x > th => x = 0
            self._data = self._data + dt/tau*(-self._data + h + aff ) +  1/tau*delta*lat + noise
            
        else:
            raise Exception("Invalid model option : " + model)

        if resetLat:
                self.getChild('lat').resetLat()
