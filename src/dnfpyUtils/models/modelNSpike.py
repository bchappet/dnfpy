from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.cellular.mapDNFNSpike import MapDNFNSpike
import warnings
import numpy as np

class ModelNSpike(Model,Renderable):
    def initMaps(self,size,nspike=10,dt=0.1,rFaults=0.0,
                 #iExc=1.25,iInh=0.7,wExc=0.0043,wInh=0.1,alpha=10,h=0,tau=0.64,
                 iExc=0.46,iInh=0.41,wExc=0.11,wInh=0.42,tau=0.12,h=0,
                 model='spike',reproductible=True,cell='NSpike',clkRatio=50,routerType='prng',
                 errorType='none',errorProb=0.0000,delta=1,

                 **kwarg
                 ):
        """We initiate the map and link them"""
        #Create maps
        self.field = MapDNFNSpike("Potential",size,dt=dt,nspike=nspike,iExc=iExc,iInh=iInh,pExc=wExc,pInh=wInh,model=model,reproductible=reproductible,
                cell=cell,clkRatio=clkRatio,routerType=routerType,errorType=errorType,errorProb=errorProb,
                h=h,tau=tau,delta=delta)


        #test faults
        #faults = np.random.random((size,size)) < (rFaults)
        #self.field.lat.exc.lib.setArrayAttribute(2,faults)
        #self.field.lat.inh.lib.setArrayAttribute(2,faults)

        #return the roots
        roots =  [self.field]
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.field]
        ret.extend(self.field.getArrays())
        return ret

    #override Model
    def onAfferentMapChange(self,afferentMap):
        self.field.addChildren(aff=afferentMap)

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%((mapName),x,y))
