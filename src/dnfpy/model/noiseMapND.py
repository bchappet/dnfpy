
from dnfpy.core.funcMapND import FuncMap
import numpy as np
def randomNormal(scale,shape):
    """because np.random.normal does not support scale = 0"""
    if scale == 0:
        return np.zeros(shape,dtype=np.float32)
    else:
        #return np.random.uniform(low=-scale,high=scale,size=size_)
        return np.random.normal(0,scale,shape)


class NoiseMap(FuncMap):
        def __init__(self,name,size,dim=1,dt=0.1,intensity=0.01):
                super(NoiseMap,self).__init__(randomNormal,name,size,dim=dim,dt=dt,
                                scale=intensity,shape=(size,)*dim)
