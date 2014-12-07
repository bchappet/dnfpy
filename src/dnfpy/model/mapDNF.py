from activationMap import ActivationMap
from fieldMap import FieldMap
from lateralWeightsMap import LateralWeightsMap
from convolution import Convolution

class MapDNF(FieldMap):
    def __init__(self,name,size,dt=0.1,wrap=True,
                 tau=0.64,h=0,
                 model='cnft',th=0.75,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10,alpha=10,
                 mapSize=1.,
                 **kwargs):
        super(MapDNF,self).__init__(name,size,dt=dt,wrap=wrap,
                    tau=tau,h=h,
                    model=model,th=th,
                    **kwargs)

        self.act = ActivationMap(name+"_activation",size,dt=dt,model=model,th=th)
        self.lat =Convolution(name+"_lateral",size,dt=dt,wrap=wrap)
        self.kernel = LateralWeightsMap(name+"_kernel",mapSize=mapSize,
                                        globalSize=size,wrap=wrap,
                                        iExc=iExc,iInh=iInh,wExc=wExc,
                                        wInh=wInh,alpha=alpha)
        self.act.addChildren(field=self)
        self.addChildren(lat=self.lat)
        self.lat.addChildren(source=self.act,kernel=self.kernel)
        self.kernel.compute()
    def getActivation(self):
        return self.act

    def getArrays(self):
        return [
            self.act,
            self.lat,
            self.kernel,
        ]



