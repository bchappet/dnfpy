from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.stats.statsList import StatsList
from dnfpy.learning.learningDNFMap import LearningDNFMap
from dnfpy.model.straightTrack import StraightTrack
import numpy as np
from dnfpy.core.constantMap import ConstantMap
from dnfpy.model.noiseMap import NoiseMap

class ModelSTDP(Model,Renderable):
    def initMaps(self,size=49,nbStep=0,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10.,alpha=10.,
                 ):
        """We initiate the map and link them"""
       # print("iExc : %s, iInh: %s, wExc %s, wInh %s"%(iExc,iInh,wExc,wInh))
        #Create maps
        dt = 0.1
        wrap = True
        #self.aff = StraightTrack("input",size,dt,wrap,1.,width=0.1,
         #                           direction=np.float32([1,1]),speed=0.04)
        self.aff = InputMap("Inputs",size,noiseI=0.1,nbDistr=3)
        self.field = LearningDNFMap("DNF",size,dt=dt,sizeKernel=size,th=0.65)
        self.field.addChildren(aff=self.aff)
        #return the roots
        roots =  [self.field]
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.aff,self.field]
        ret.extend(self.field.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
