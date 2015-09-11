from dnfpy.core.funcMap2D import FuncMap2D
import numpy as np
def randomNormal(scale,size_):
    """because np.random.normal does not support scale = 0"""
    if scale == 0:
        return np.zeros(size_,dtype=np.float32)
    else:
        #return np.random.uniform(low=-scale,high=scale,size=size_)
        return np.random.normal(0,scale,size=size_)


class NoiseMap(FuncMap2D):
        def __init__(self,name,size,dt=0.1,intensity=0.01):
                super(NoiseMap,self).__init__(randomNormal,name,size,dt=dt,
                                scale=intensity,size_=(size,size))
