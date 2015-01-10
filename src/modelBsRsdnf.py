from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.cellular.mapDNFBsRsdnf import MapDNFBsRsdnf

class ModelBsRsdnf(Model,Renderable):
    def initMaps(self,size):
        """We initiate the map and link them"""
        dt = 0.001

        #Create maps
        self.aff = InputMap("Inputs",size,dt=dt)
        self.field = MapDNFBsRsdnf("DNF",size,dt=dt)
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
