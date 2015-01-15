from dnfpy.model.activationMap import ActivationMap
import numpy as np
from dnfpy.model.fieldMap import FieldMap
from dnfpy.cellular.bsRsdnfConvolution import BsRsdnfConvolution

class MapDNFBsRsdnf(FieldMap):
    def __init__(self,name,size,dt=0.1,wrap=True,
                 tau=0.64,h=0,routerType="orRouter",
                 th=0.75,sizeStream=1000,pSpike=0.01,
                 iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.5,alpha=10,
                 **kwargs):
        super(MapDNFBsRsdnf,self).__init__(name,size,dt=dt,wrap=wrap,
                    tau=tau,h=h,
                    model='spike',th=th,
                    **kwargs)

        self.act = ActivationMap(name+"_activation",size,dt=dt,model='spike',
                                 dtype=np.intc,th=th)
        self.lat = BsRsdnfConvolution(name+"_spikePropag.",size,dt=dt,
                                      sizeStream=sizeStream,pSpike=pSpike,
                                      routerType=routerType,
                                        pExc=pExc,pInh=pInh,iExc=iExc,
                                        iInh=iInh,alpha=alpha)
        self.act.addChildren(field=self)
        self.addChildren(lat=self.lat)
        self.lat.addChildren(activation=self.act)
    def getActivation(self):
        return self.act

    def getArrays(self):
        return [
            self.act,
            self.lat,
        ]



