from dnfpy.core.mapND import MapND
import numpy as np
from dnfpy.model.noiseMapND import NoiseMap

class FieldMap(MapND):
    def __init__(self,name,size,dim=1,dt=0.1,model='cnft',tau=0.64,h=0.0,th=0.75,delta=1.,
                    resetLat=False,gainAff=1.0,afferentInhibition=0.0,wAffInh=1.0,
                    noiseI=0.0,leak=1.0,
                    sfa=0,beta=1.0,
                    **kwargs):
        """
        Parameters:
           afferentInhibition : will be integrated as a negative contribution to the potential 
        """
        super().__init__(name,size,dim=dim,dt=dt,model=model,
                                      tau=tau,h=h,th=th,delta=delta,leak=leak,
                                      resetLat=resetLat,gainAff=gainAff,noiseI=noiseI,
                                      afferentInhibition=afferentInhibition,wAffInh=wAffInh,
                                      sfa=sfa,beta=beta,
                                      **kwargs)

        self.noise = NoiseMap(name+"_noise",size=size,dim=dim,dt=dt,intensity=noiseI)
        self.addChildren(noise=self.noise)



    def _compute(self,model,lat,aff,dt,tau,h,th,leak,delta,resetLat,gainAff,noise,afferentInhibition,wAffInh,sfa,beta):
        if model == 'cnft':
            self._data = self._data + dt/tau*(-leak*self._data + h + aff*gainAff + delta*lat - afferentInhibition*wAffInh - beta*sfa) + noise
        elif model == 'spike':
            self._data = np.where(self._data > th,h,self._data) # if x > th => x = h
            self._data = self._data + dt/tau*(-leak*self._data + h + aff*gainAff - afferentInhibition -beta*sfa) +  1.0/tau*delta*lat + noise
        elif model == 'event': #we suppose that every feeding is a spike
            self._data = np.where(self._data > th,h,self._data) # if x > th => x = h
            self._data = self._data + dt/tau*(-leak*self._data + h)+ 1.0/tau*(aff*gainAff - afferentInhibition+delta*lat - beta*sfa) + noise
        elif model == 'pulse':
            self._data = np.where(self._data > th,h,self._data) # if x > th => x = h
            tau_vec = np.where(self._data > h,tau,-tau)
            tau_vec[self._data == h] = 0
            self._data = self._data + aff + lat - tau_vec
        else:
            print("Invalid model option : " + model)

        if resetLat:
                self.getChild('lat').resetLat()
