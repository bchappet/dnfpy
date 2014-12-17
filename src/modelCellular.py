from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.core.map2D import Map2D
import numpy as np
import numpy.ctypeslib as npct
from ctypes import c_int
from ctypes import CFUNCTYPE
from ctypes import POINTER
from ctypes import c_ubyte
libac = npct.load_library("libac", "dnfpy/cellular/lib/")

class CellMap(Map2D):
        def __init__(self,name,size,depth=1,**kwargs):
            super(CellMap,self).__init__(name,size,depth=depth,**kwargs)
            CELL_FUNC = CFUNCTYPE(None, POINTER(c_ubyte), POINTER(POINTER(c_ubyte)))
            self.cell_fun_c = libac.compute_cell
            self.cell_fun_c.argtypes = [POINTER(c_ubyte),POINTER(POINTER(c_ubyte))]
            self.func = libac.synchronous_step
            self.func.argtypes = [
                        np.ctypeslib.ndpointer(dtype=np.uint8,ndim=3,flags='C_CONTIGUOUS'),
                        np.ctypeslib.ndpointer(dtype=np.uint8,ndim=3,flags='C_CONTIGUOUS'),
                        c_int,c_int,c_int,CELL_FUNC]
            self.cell_fun = CELL_FUNC(self.game_life_func)

        def game_life_func(self,data,neighs):
            self.cell_fun_c(data,neighs)

        def _compute(self,size,depth):
                nextBuff = (self.current+1) % len(self._buffers)
                self.func(self._buffers[self.current],
                          self._buffers[nextBuff],
                          size,size,depth,self.cell_fun)
                self._data = self._buffers[nextBuff]
                self.current = nextBuff


        def reset(self):
                size = self.getArg('size')
                depth = self.getArg('depth')
                rand = np.random.rand(size,size)
                self.current = 0
                buffer1 = np.where(rand > 0.5,1.,0.)
                buffer1 = buffer1.astype(dtype=np.uint8)
                buffer1 = buffer1.reshape((size,size,depth))
                buffer2 = np.copy(buffer1)
                self._buffers = [buffer1,buffer2]
                self._data = self._buffers[self.current]


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
