from activationMap import ActivationMap
import numpy as np
from fieldMap import FieldMap
from lateralWeightsMap import LateralWeightsMap
from dnfpy.core.map2D import Map2D
from convolution import Convolution


class  AffSFA(Map2D):
    def __init__(self,name,size,dt,beta):
        super(AffSFA,self).__init__(name,size,dt=dt,beta=beta)

    def _compute(self,beta,input,sfa):
        self._data = ((1-beta))*2*input - (beta)*2*sfa

class SFAMap(Map2D):
    def __init__(self,name,size,dt,tau=1.,m=6.4):
        super(SFAMap,self).__init__(name=name,size=size,dt=dt,tau=tau,m=m)

    def _compute(self,pot,tau,dt,m):
        self._data = self._data + dt/tau*(-self._data + m*pot)


class MapSFA(Map2D):
    def __init__(self,name,size,dt=0.1,wrap=True,
                 tau=0.64,h=0,
                 model='cnft',th=0.75,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10,alpha=10,
                 mapSize=1.,nbStep=0,beta=0.2,m=1.1,tauSFA=2.8,
                 **kwargs):
        super(MapSFA,self).__init__(name,size,dt=dt,wrap=wrap,
                    tau=tau,h=h,
                    model=model,th=th,
                    beta=beta,
                    **kwargs)

        self.act = ActivationMap(name+"_activation",size,dt=dt,model=model,th=th)



        self.sfa = SFAMap("SFA",size,dt=dt,tau=tauSFA,m=m)
        self.sfa.addChildren(pot=self)


        self.lat =Convolution(name+"_lateral",size,dt=dt,wrap=wrap)
        self.kernel = LateralWeightsMap(name+"_kernel",mapSize=mapSize,
                                        globalSize=size,wrap=wrap,
                                        iExc=iExc,iInh=iInh,wExc=wExc,
                                        wInh=wInh,alpha=alpha,nbStep=nbStep)
        self.act.addChildren(field=self)
        self.addChildren(lat=self.lat,sfa=self.sfa)
        self.lat.addChildren(source=self.act,kernel=self.kernel)

    def _compute(self,model,lat,aff,dt,tau,h,th,sfa,beta):
        aff_sfa = ((1-beta))*2*aff - (beta)*2*sfa

        if model == 'cnft':
            self._data = self._data + dt/tau*(-self._data + h + aff_sfa + lat)
        elif model == 'spike':
            self._data = np.where(self._data > th,0.,self._data) # if x > th => x = 0
            self._data = self._data + dt/tau*(-self._data + h + aff_sfa ) +  1/tau*lat
        else:
            print "Invalid model option : " + model

    def getActivation(self):
        return self.act

    def getArrays(self):
        return [
            self.act,
            self.lat,
            self.sfa,
        ]
