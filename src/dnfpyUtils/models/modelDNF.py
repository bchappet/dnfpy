from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNFND import MapDNFND
from dnfpy.model.mapDNF import MapDNF

class ModelDNF(Model,Renderable):
    """
    For DOG:
        {'iExc' : 1.25,'iInh' : 0.7,'wExc' : 0.1,'wInh': 0.9}
    For DOE:
        {'wExc' : 0.0043, 'wInh':0.9}
    For DOL:
        {'iExc' : 0.15,'iInh' : 0.65,'wExc' : 9.16, 'wInh' : 1.10}



    """
    def initMaps(self,size=49,model="cnft",activation="step",nbStep=0,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10.,alpha=10.,th=0.75,h=0,lateral='dog',noiseI=0.01,
                 dt=0.1,
                 ):
        """We initiate the map and link them"""
       # print("iExc : %s, iInh: %s, wExc %s, wInh %s"%(iExc,iInh,wExc,wInh))
        #Create maps
        self.aff = InputMap("Inputs",size,dt=dt,noiseI=noiseI)
                            #iStim1 = 0, iStim2 = 0,noiseI=1.,noise_dt=1e10)
               
        self.field = MapDNFND("Potential",size,dt=dt,dim=2,model=model,activation=activation,nbStep=nbStep, \
                        iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh,th=th,h=h,lateral=lateral)
        self.field.addChildren(aff=self.aff)
        #return the roots
        roots =  [self.field]
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.aff,self.field,self.field.kernel]
        ret.extend(self.field.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
