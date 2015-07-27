from dnfpy.model.activationMap import ActivationMap
import numpy as np
from dnfpy.model.fieldMap import FieldMap
from dnfpy.cellular.bsRsdnfConvolution import BsRsdnfConvolution
from dnfpy.cellular.sbsFastConvolution import SbsFastConvolution
from dnfpy.cellular.sbsFast2LayerConvolution import SbsFast2LayerConvolution

class MapDNFBsRsdnf(FieldMap):
    def __init__(self,name,size,dt=0.1,dtPropagation=0.0001,wrap=True,
                 tau=0.64,h=0,routerType="orRouter",mapType="doublefast",
                 precisionProba=30,
                 th=0.75,sizeStream=1000,pSpike=0.01,
                 iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.5,alpha=10,
                 reproductible=True, shift=5,nbSharedBit=31,
                 **kwargs):
        super(MapDNFBsRsdnf,self).__init__(name,size,dt=dt,wrap=wrap,
                    tau=tau,h=h,
                    model='spike',th=th,mapType=mapType,
                    **kwargs)

        self.act = ActivationMap(name+"_activation",size,dt=dt,model='spike',
                                 dtype=np.intc,th=th)
        if mapType == "doublefast":
            self.lat = SbsFast2LayerConvolution(name+"_spikePropag.",size,dt=dtPropagation,
                                      sizeStream=sizeStream,pSpike=pSpike,
                                      precisionProba=precisionProba,
                                      routerType=routerType,
                                        pExc=pExc,pInh=pInh,iExc=iExc,
                                        iInh=iInh,alpha=alpha,
                                      reproductible=reproductible,
                                                shift=shift,nbSharedBit=nbSharedBit)
        elif mapType == "fast":
            self.lat = SbsFastConvolution(name+"_spikePropag.",size,dt=dtPropagation,
                                      sizeStream=sizeStream,pSpike=pSpike,
                                      precisionProba=precisionProba,
                                      routerType=routerType,
                                        pExc=pExc,pInh=pInh,iExc=iExc,
                                        iInh=iInh,alpha=alpha,
                                      reproductible=reproductible)
        elif mapType == "slow":
            self.lat = BsRsdnfConvolution(name+"_spikePropag.",size,dt=dtPropagation,
                                      sizeStream=sizeStream,pSpike=pSpike,
                                      precisionProba=precisionProba,
                                      routerType=routerType,
                                        pExc=pExc,pInh=pInh,iExc=iExc,
                                        iInh=iInh,alpha=alpha,
                                      reproductible=reproductible)
        else:
            print("This map type : %s is not available"%mapType)
            exit()

        self.act.addChildren(field=self)
        self.addChildren(lat=self.lat)
        self.lat.addChildren(activation=self.act)

    def _compute(self,model,lat,aff,dt,tau,h,th,mapType):
        self._data = np.where(self._data > th,0.,self._data) # if x > th => x = 0
        self._data = self._data + dt/tau*(-self._data + h + aff ) +  1/tau*lat
        #reset lateral field
        if mapType == "slow":
            self.lat.resetData()

    def getActivation(self):
        return self.act

    def getArrays(self):
        return [
            self.act,
            self.lat,
        ]
