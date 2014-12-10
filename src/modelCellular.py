from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNF import MapDNF
from dnfpy.core.map2D import Map2D
import cmod
import numpy as np

class CellMap(Map2D):
        def _compute(self):
                cmod.syncUpdate(self._data)
        def reset(self):
                size = self.getArg('size')
                rand = np.random.rand(size,size)
                self._data = np.where(rand > 0.5,1.,0.)


class ModelCellular(Model,Renderable):
    def initMaps(self,size):
        """We initiate the map and link them"""
        #Create maps
        self.map = CellMap("CellMap",size=size,dt=0.1)
        return self.map
    #override Renderable
    def getArrays(self):
        ret =  [self.map]
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
