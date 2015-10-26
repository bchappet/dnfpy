import numpy as np
import sys
import math
from dnfpy.core.computable import Computable
from dnfpy.core.mapND import MapND
import inspect


class Map2D(MapND):
    """
    The Map2D will be updated when simuTime = self.time + self.dt
    The allowed precision for the time values is 1e-10

    Attributes:
        'size': the data is of shape (size,size)
        'dt':  the update will be done every dt (second)
        'time': simulation time
        self._data: data accessible with self.getData()

    Methods:
        _compute: abstract define the beahaviour of the map here.
            Use any attribute or child in the method parameter
            Set self._data to finalize the computation

        _onParamUpdate: abstract called whenever self.setArg is called
            Use any attribute in the method parameters

        compute: compute the children state and the self state without updating
            self.time

        update(compTime): update the children a then self
            if compTime = self.__getNextUpdateTime

        getSmallestNextUpdateTime: get the smallest self.time + self.dt whithin
        self and the children

    """

    def __init__(self,name,size,dtype=np.float32,**kwargs):
        super(Map2D,self).__init__(name,size=size,dtype=dtype,dim=2,**kwargs)


