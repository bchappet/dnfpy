from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNF import MapDNF
from dnfpy.stats.statsList import StatsList

class ModelDNF(Model,Renderable):
    def initMaps(self,size=49,model="cnft",nbStep=0,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10.,alpha=10.,th=0.75,
                 ):
        """We initiate the map and link them"""
       # print("iExc : %s, iInh: %s, wExc %s, wInh %s"%(iExc,iInh,wExc,wInh))
        #Create maps
        self.aff = InputMap("Inputs",size)
                            #iStim1 = 0, iStim2 = 0,noiseI=1.,noise_dt=1e10)
        self.field = MapDNF("DNF",size,model=model,nbStep=nbStep, \
                        iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh,th=th)
        self.field.addChildren(aff=self.aff)
        #stats
        self.stats = StatsList(size,self.aff,self.field.getActivation(),
                               self.field,shapeType='gauss')
        #return the roots
        roots =  [self.field]
        roots.extend(self.stats.getRoots())
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.aff,self.field]
        #ret.extend(self.field.getArrays())
        ret.extend(self.stats.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
