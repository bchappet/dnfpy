
import numpy as np
import dnfpy.core.utils as utils
from  dnfpy.core.funcMap2D import FuncMap2D
from dnfpy.core.map2D import Map2D
import random

class DistrMap(Map2D):
        def __init__(self,name,size,dt=1.,wrap=True,intensity=0,number=0,width=0.1,
                     ):
                super(DistrMap,self).__init__(name,size,dt=dt,wrap=wrap,
                                intensity=intensity,number=number,width=width,
                                              )

        def _compute(self,size,wrap,intensity,width,number,dtype):
                self._data = np.zeros((size,size),dtype=dtype)
                for i in range(number):
                        cx = random.uniform(0,size-1)
                        cy = random.uniform(0,size-1)
                        distrI = utils.gauss2d(size,wrap,intensity,width,cx,cy)
                        self._data = self._data + distrI



