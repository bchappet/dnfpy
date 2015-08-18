from dnfpy.core.mapND import MapND
import numpy as np
from dnfpy.model.noiseMapND import NoiseMap

class FieldMapND(MapND):
    def __init__(self,name,size,dt=0.1,model='cnft',tau=0.64,h=0,th=0.75,delta=1.,
                    resetLat=False,gainAff=1.0,
                    noiseI=0.0,
                    **kwargs):
        super(FieldMapND,self).__init__(name,size,dt=dt,model=model,
                                      tau=tau,h=h,th=th,delta=delta,
                                      resetLat=resetLat,gainAff=gainAff,noiseI=noiseI,**kwargs)

        self.noise = NoiseMap(name+"_noise",size=size,dt=dt,intensity=noiseI)
        self.addChildren(noise=self.noise)


    def _compute(self,model,lat,aff,dt,tau,h,th,delta,resetLat,gainAff,noise):
        if model == 'cnft':
            self._data = self._data + dt/tau*(-self._data + h + aff*gainAff + delta*lat) + noise
        elif model == 'spike':
            self._data = np.where(self._data > th,0.,self._data) # if x > th => x = 0
            self._data = self._data + dt/tau*(-self._data + h + aff*gainAff ) +  1.0/tau*delta*lat + noise
        else:
            print "Invalid model option : " + model

        if resetLat:
                self.getChild('lat').resetLat()
