from dnfpy.core.map2D import Map2D
import numpy as np


class CellularMap(Map2D):
    """
    This map is used as a super class for all the cellular compution
    A conmputation function can be provided
    Or this map can be extended

    """
    def __init__(self,name,size,computation=None,dt=0.1,dtype=np.uint8,**kwargs):
        super(CellularMap,self).__init__(name,size,dtype,dt=dt,computation=computation,**kwargs)



    def _compute(self,computation):
        self._data = computation(self._data)

    def init(self,size):
        return np.random.randint(0,2,(size,size))


    def reset(self):
        super(CellularMap,self).reset()
        size = self._init_kwargs['size']
        dtype = self._init_kwargs['dtype']
        self._data = self.init(size)

    def onClick(self,x,y):
        self._data[y,x]  = (self._data[y,x]+1)%2

    def getArrays(self):
        return [self,]






