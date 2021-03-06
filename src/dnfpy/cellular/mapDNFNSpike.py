from dnfpy.model.activationMap import ActivationMap
import numpy as np
from dnfpy.model.fieldMapND import FieldMap
from dnfpy.cellular.nSpikeConvolution import NSpikeConvolution
from dnfpy.cellular.rsdnf2LayerConvolution import Rsdnf2LayerConvolution

class MapDNFNSpike(FieldMap):
    def __init__(self,name,size,dt=0.1,wrap=True,
                 tau=0.64,h=0,
                 th=0.75,nspike=20,model='spike',
                 iExc=1.25,iInh=0.7,wExc=0.0043,wInh=0.9,alpha=10,reproductible=True,
                 cell = 'NSpike',clkRatio=400,routerType='prng',shift=10,
                 errorType='none',errorProb=0.0001,
                 **kwargs):
        super(MapDNFNSpike,self).__init__(name,size,dim=2,dt=dt,wrap=wrap,tau=tau,h=h,th=th,nspike=nspike,model=model,iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh,alpha=alpha,reproductible=reproductible,cell=cell,routerType=routerType,
                errorType=errorType,errorProb=errorProb,
                **kwargs)
        if cell == 'Rsdnf' or cell == 'Rsdnf2' :
            self.setArg(resetLat =True) #we need to reset the lateral wieight for  every new compuation

        self.act = ActivationMap("Activation",size,dt=dt,type='step',
                                 dtype=np.intc,th=th)
        if cell == 'Rsdnf2':
            self.lat = Rsdnf2LayerConvolution("Lateral",size,dt=dt,nspike=nspike,
                                    pExc=wExc,pInh=wInh,iExc=iExc,
                                    iInh=iInh,alpha=alpha,reproductible=reproductible
                                    ,cell=cell,clkRatio=clkRatio,shift=shift)
        else:
            self.lat = NSpikeConvolution("Lateral",size,dt=dt,nspike=nspike,
                                    wExc=wExc,wInh=wInh,iExc=iExc,
                                    iInh=iInh,alpha=alpha,reproductible=reproductible,cell=cell,clkRatio=clkRatio,routerType=routerType,
                                    errorType=errorType,errorProb=errorProb)

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



