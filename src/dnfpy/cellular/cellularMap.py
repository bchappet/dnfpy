from dnfpy.core.map2D import Map2D
from ctypes import c_int
from ctypes import CFUNCTYPE
from ctypes import POINTER
from ctypes import c_ubyte
import numpy as np
import numpy.ctypeslib as npct
libac = npct.load_library("libac", "dnfpy/cellular/lib/")

class CellularMap(Map2D):
        def __init__(self,c_func,name,size,depth=1,**kwargs):
            super(CellularMap,self).__init__(name=name,
                                            size=size,depth=depth,
                                            **kwargs)
            CELL_FUNC = CFUNCTYPE(None, POINTER(c_ubyte), POINTER(POINTER(c_ubyte)))
            self.c_func = c_func
            self.c_func.argtypes = [POINTER(c_ubyte),POINTER(POINTER(c_ubyte))]
            self.func = libac.synchronous_step
            self.func.argtypes = [
                            np.ctypeslib.ndpointer(dtype=np.uint8,ndim=3,flags='C_CONTIGUOUS'),
                            np.ctypeslib.ndpointer(dtype=np.uint8,ndim=3,flags='C_CONTIGUOUS'),
                            c_int,c_int,c_int,CELL_FUNC]
            self.cell_fun = CELL_FUNC(self.cellular_func)

        def cellular_func(self,data,neighs):
            self.c_func(data,neighs)

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
