
from dnfpy.model.inputMap1D import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNFND import MapDNFND
from dnfpy.core.constantMapND import ConstantMapND
import numpy as np

class ModelDNF1D(Model,Renderable):
    def initMaps(self,size=49,model="cnft",activation="step",nbStep=0,dim=1,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10.,alpha=10.,th=0.75,h=0,
                 ):
        """We initiate the map and link them"""
       # print("iExc : %s, iInh: %s, wExc %s, wInh %s"%(iExc,iInh,wExc,wInh))
        #Create maps
        self.aff = InputMap("Inputs",size,dim=dim,periodStim=36,iStim1 = 1,iStim2=0 )
        #input = np.zeros((size))
        #input[size/2] = 1
        #self.aff = ConstantMapND("Inputs",size,value=input)
               
        self.field = MapDNFND("Potential",size,dim=dim,model=model,activation=activation,nbStep=nbStep, \
                        iExc=3.7,iInh=iInh,wExc=0.05,wInh=0.1,th=0.75,h=h,tau=0.1)
        self.field.addChildren(aff=self.aff)
        #return the roots
        roots =  [self.field]
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.aff,self.field,self.field.act,self.field.lat,self.field.kernel,]
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
