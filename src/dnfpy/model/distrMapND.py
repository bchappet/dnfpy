
import numpy as np
import dnfpy.core.utils as utils
from  dnfpy.core.funcMapND import FuncMapND
from dnfpy.core.mapND import MapND
import random

class DistrMap(MapND):
        def __init__(self,name,size,dt=1.,wrap=True,intensity=0,number=0,width=0.1,
                     ):
                super(DistrMap,self).__init__(name,size,dt=dt,wrap=wrap,
                                intensity=intensity,number=number,width=width,
                                              )

        def _compute(self,size,wrap,intensity,width,number,dtype):
                self._data = np.zeros((size),dtype=dtype)
                for i in range(number):
                        cx = random.uniform(0,size-1)
                        distrI = utils.gaussNd(size,wrap,intensity,width,cx)
                        self._data = self._data + distrI



