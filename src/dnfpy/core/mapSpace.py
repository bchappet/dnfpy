import numpy as np
from dnfpy.core.mapND import MapND


def getDx(space):
        xMin = np.min(space[0])
        xMax = np.max(space[0])
        size = size=space[0].shape[0]
        tmp,dx = np.linspace(xMin,xMax,size,retstep=True)
        return dx


class MapSpace(MapND):
    def __init__(self,name,space,dtype=np.float32,**kwargs):
        super().__init__(name,space[0].shape[0],dim=len(space),dtype=dtype,space=space,dx=getDx(space),**kwargs)
