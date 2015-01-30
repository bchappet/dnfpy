from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNF import MapDNF

class ModelDNF(Model,Renderable):
    def initMaps(self,size):
        """We initiate the map and link them"""
        #Create maps
        self.aff = InputMap("Inputs",size)
        self.field = MapDNF("DNF",size)
        self.field.addChildren(aff=self.aff)
        #return the root
        return self.field
    #override Renderable
    def getArrays(self):
        ret =  [self.aff,self.field]
        ret.extend(self.field.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
