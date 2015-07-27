from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNF import MapDNF
from dnfpy.stats.statsList import StatsList
from dnfpy.model.fieldMap import FieldMap
from dnfpy.model.activationMap import ActivationMap
from dnfpyUtils.cellular.hppReaction import HppReaction
import numpy as np

class ModelDNFHppReact(Model,Renderable):
    def initMaps(self,size=49,dt=0.1,model="spike",
                 iExc=1.25,iInh=0.7,rho=0.3
                 ):
        """We initiate the map and link them"""
       # print("iExc : %s, iInh: %s, wExc %s, wInh %s"%(iExc,iInh,wExc,wInh))
        #Create maps
        self.aff = InputMap("Inputs",size,dt=dt)
                            #iStim1 = 0, iStim2 = 0,noiseI=1.,noise_dt=1e10)
        self.field = FieldMap("DNF",size,dt=dt,model=model,resetLat=True)


        self.act = ActivationMap("activation",size,dt=dt,model=model,dtype=np.bool_)
        self.act.addChildren(field=self.field)


        dtLat = dt/(size*2+10)
        self.lat = HppReaction("lat",size,dnfSize=size,dt=dtLat,iExc=iExc,iInh=iInh,rho=rho)

        self.lat.addChildren(activation=self.act)

        self.field.addChildren(aff=self.aff,lat=self.lat)
        #stats
        self.stats = StatsList(size,self.aff,self.act,
                               self.field,shapeType='gauss')
        #return the roots
        roots =  [self.field]
        roots.extend(self.stats.getRoots())
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.aff,self.field,self.act,self.lat]
        ret.extend(self.stats.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
