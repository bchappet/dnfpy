from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.core.map2D import Map2D
import numpy as np
import numpy.ctypeslib as npct
from dnfpy.cellular.cellularMap import CellularMap
libac = npct.load_library("libac", "dnfpy/cellular/lib/")

class ModelCellular(Model,Renderable):
    def initMaps(self,size):
        """We initiate the map and link them"""
        #Create maps
        self.map = CellularMap(libac.compute_cell,"CellMap",size,
                               dt=0.1)
        return self.map
    #override Renderable
    def getArrays(self):
        ret =  [self.map]
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
