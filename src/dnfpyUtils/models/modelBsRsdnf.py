from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.cellular.mapDNFBsRsdnf import MapDNFBsRsdnf
from dnfpy.stats.statsList import StatsList

class ModelBsRsdnf(Model,Renderable):
    def initMaps(self,size,dt=0.001,sizeStream=500):
        """We initiate the map and link them"""

        #Create maps
        self.aff = InputMap("Inputs",size,dt=dt)
        #WM
        #self.field = MapDNFBsRsdnf("DNF",size,dt=dt,sizeStream=100,iExc=0.9,pInh=0.02)
        self.field = MapDNFBsRsdnf("DNF",size,dt=dt,sizeStream=sizeStream)
        self.field.addChildren(aff=self.aff)
        #stats
        self.stats = StatsList(size,self.aff,self.field.getActivation(),dt=dt)
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
