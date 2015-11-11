
from dnfpy.model.inputMap1D import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNFND import MapDNFND
from dnfpy.core.constantMapND import ConstantMapND
import numpy as np
from dnfpy.model.mapCNNDNF import MapCNNDNF

class ModelCNNDNF(Model,Renderable):
    def initMaps(self,size=49,model="cnft",activation="id",nbStep=0,dim=2,
                 iExc=0.6,iInh=100.,wExc=0.5,wInh=2.4,th=0.75,h=0,noiseI=0.01,
                 iStim1=1.,dt=0.01,
                 ):
        """We initiate the map and link them"""
       # print("iExc : %s, iInh: %s, wExc %s, wInh %s"%(iExc,iInh,wExc,wInh))
        #Create maps
        self.aff = InputMap("Inputs",size,dim=dim,dt=dt,periodStim=36,tck_radius=0.3,iStim1 = iStim1,iStim2=1.0,noiseI=noiseI,straight=False)
        #input = np.zeros((size))
        #input[size/2] = 1
        #self.aff = ConstantMapND("Inputs",size,value=input)
               
        self.field = MapCNNDNF("Potential",size,dim=dim,dt=dt,model=model,activation=activation,nbStep=nbStep,
               iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh,th=th,h=h,gainAff=1)
        self.field.addChildren(aff=self.aff)
        #return the roots
        roots =  [self.field]
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.aff,self.field,self.field.act,self.field.lat,self.field.lat.kernelExc,self.field.lat.kernelInh]
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
