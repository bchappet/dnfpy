from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNF import MapDNF
from dnfpy.stats.statsList import StatsList
from dnfpyUtils.cellular.hppMap import HppMap

import dnfpy.core.utils as utils
from dnfpy.core.map2D import Map2D


class Lateral(Map2D):
        def _compute(self,exc,inh,delta):
                self._data = delta*(1 * exc - 2 * inh)

class ModelHPP(Model,Renderable):
    def initMaps(self,size=49,model="spike",nbStep=0,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10.,alpha=10.,
                 ):
        """We initiate the map and link them"""
        # print("iExc : %s, iInh: %s, wExc %s, wInh %s"%(iExc,iInh,wExc,wInh))
        dt = 0.1
        self.aff = InputMap("Inputs",size)
                            #iStim1 = 0, iStim2 = 0,noiseI=1.,noise_dt=1e10)
        self.field = MapDNF("DNF",size,model=model,nbStep=nbStep, \
                        iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh)
        self.field.addChildren(aff=self.aff)

        dt2 = 0.01
        self.lat = Lateral("Lateral",size,dt=dt2,delta=0.02)  
        self.exc = HppMap("exc",size,dt=dt2)
        self.inh = HppMap("inh",size,dt=dt2)
        self.lat.addChildren(exc=self.exc,inh=self.inh)


        self.field.lat = self.lat
        self.field.addChildren(lat=self.field.lat)
        self.exc.addChildren(source=self.field.act)
        self.inh.addChildren(source=self.field.act)

        #stats
        #self.stats = StatsList(size,self.aff,self.field.getActivation(),
        #                       self.field,shapeType='gauss')
        #return the roots
        roots =  [self.field]
        #roots.extend(self.stats.getRoots())
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.aff,self.field,self.exc,self.inh]
        ret.extend(self.field.getArrays())
        #ret.extend(self.stats.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
