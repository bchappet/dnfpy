
from dnfpy.model.inputMap1D import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNFND import MapDNFND
from dnfpy.core.constantMapND import ConstantMapND
import numpy as np
import dnfpy.core.utilsND as utils
from dnfpy.core.funcMapND import FuncMap

class ModelBubbleShift1D(Model,Renderable):
    """
    We are trying to show that it is possible to push a bubble with a string inhibbition
    """
    def initMaps(self,size=49,model="cnft",activation="step",nbStep=0,
                 iExc=3.5,iInh=0.7,wExc=0.1,wInh=1.,alpha=10.,th=0.75,h=0,
                 ):
        """We initiate the map and link them"""
       # print("iExc : %s, iInh: %s, wExc %s, wInh %s"%(iExc,iInh,wExc,wInh))
        #Create maps
        self.aff = InputMap("Inputs",size,periodStim=20000,iStim1 = 0 )
        #input = np.zeros((size))
        #input[size/2] = 1
        #self.aff = ConstantMapND("Inputs",size,value=input)

        self.inh = FuncMap(utils.gaussNd,"inh",size,dt=0.1,center=size/2,
                              wrap=True,intensity=-1.,width=0.1*size)
        self.aff.addChildren(self.inh)
               
        self.field = MapDNFND("Potential",size,model=model,activation=activation,nbStep=nbStep, \
                        iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh,th=th,h=h)
        self.field.addChildren(aff=self.aff)
        #return the roots
        roots =  [self.field]
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.aff,self.field,self.field.act,self.field.lat,self.field.kernel,self.inh]
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
