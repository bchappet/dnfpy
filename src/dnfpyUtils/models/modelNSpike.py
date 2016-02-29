from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.cellular.mapDNFNSpike import MapDNFNSpike
import warnings
import numpy as np

class ModelNSpike(Model,Renderable):
    def initMaps(self,size,nspike=10,dt=0.1,rFaults=0.0,
                 iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.9,alpha=10,
                 model='spike',reproductible=True,cell='NSpike',clkRatio=50,routerType='prng',
                 **kwarg
                 ):
        """We initiate the map and link them"""
        #Create maps
        self.field = MapDNFNSpike("Potential",size,dt=dt,nspike=nspike,iExc=iExc,iInh=iInh,pExc=pExc,pInh=pInh,model=model,reproductible=reproductible,
                cell=cell,clkRatio=clkRatio,routerType=routerType)


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

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
