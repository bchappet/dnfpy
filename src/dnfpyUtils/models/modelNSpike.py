from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.cellular.mapDNFNSpike import MapDNFNSpike
from dnfpy.stats.statsList import StatsList

class ModelNSpike(Model,Renderable):
    def initMaps(self,size,nspike=10,
                 iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.9,alpha=10
                 ):
        """We initiate the map and link them"""
        #Create maps
        self.aff = InputMap("Inputs",size)
        self.field = MapDNFNSpike("DNF",size,nspike=nspike,iExc=iExc,iInh=iInh,pExc=pExc,pInh=pInh)
        self.field.addChildren(aff=self.aff)
        #stats
        self.stats = StatsList(size,self.aff,self.field.getActivation(),
                               self.field,shapeType='exp')

        #return the roots
        roots =  [self.field]
        roots.extend(self.stats.getRoots())
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.aff,self.field]
        ret.extend(self.field.getArrays())
        ret.extend(self.stats.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
