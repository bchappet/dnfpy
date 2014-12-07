from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNF import MapDNF

class ModelDNFdual(Model,Renderable):
    def initMaps(self,size):
        """We initiate the map and link them"""
        #Create maps
        self.aff = InputMap("Inputs",size)
        self.fieldCNFT = MapDNF("CNFT",size,model='cnft')
        self.fieldSpike = MapDNF("SpikingDNF",size,model='spike')
        self.fieldCNFT.addChildren(aff=self.aff)
        self.fieldSpike.addChildren(aff=self.aff)
        self.field =  [self.fieldCNFT,self.fieldSpike]
        #return the root
        return self.field
    #override Renderable
    def getArrays(self):
        ret =  [self.aff,self.fieldCNFT,self.fieldSpike]
        ret.extend(self.fieldCNFT.getArrays())
        ret.extend(self.fieldSpike.getArrays())
        return ret
