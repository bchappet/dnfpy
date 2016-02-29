from dnfpy.model.activationMap import ActivationMap
import numpy as np
from dnfpy.model.fieldMap import FieldMap
from dnfpy.cellular.nSpikeConvolution import NSpikeConvolution

class MapDNFNSpike(FieldMap):
    def __init__(self,name,size,dt=0.1,wrap=True,
                 tau=0.64,h=0,
                 th=0.75,nspike=20,model='spike',
                 iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.9,alpha=10,reproductible=True,
                 cell = 'NSpike',clkRatio=50,routerType='prng',
                 **kwargs):
        super(MapDNFNSpike,self).__init__(name,size,dt=dt,wrap=wrap,tau=tau,h=h,th=th,nspike=nspike,model=model,iExc=iExc,iInh=iInh,pExc=pExc,pInh=pInh,alpha=alpha,reproductible=reproductible,cell=cell,routerType=routerType,**kwargs)
        if cell is 'Rsdnf' :
            self.setArg(resetLat =True) #we need to reset the lateral wieight for  every new compuation

        self.act = ActivationMap("Activation",size,dt=dt,type='step',
                                 dtype=np.intc,th=th)
        self.lat = NSpikeConvolution("Lateral",size,dt=dt,nspike=nspike,
                                    pExc=pExc,pInh=pInh,iExc=iExc,
                                    iInh=iInh,alpha=alpha,reproductible=reproductible,cell=cell,clkRatio=clkRatio,routerType=routerType)

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



