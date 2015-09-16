from dnfpy.core.map2D import Map2D
import numpy as np
class NoiseMap(Map2D):
        def __init__(self,name,size,dt=0.1,intensity=0.01):
                super().__init__(name,size,dt=dt,
                                scale=intensity)


        def _compute(self,scale,size):
            """because np.random.normal does not support scale = 0"""
            if scale == 0:
                self._data= np.zeros((size,size),dtype=np.float32)
            else:
                #return np.random.uniform(low=-scale,high=scale,size=size_)
                self._data= np.random.normal(0,scale,size=(size,size))



