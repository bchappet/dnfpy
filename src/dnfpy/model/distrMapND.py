
import numpy as np
import dnfpy.core.utilsND as utils
from  dnfpy.core.funcMapND import FuncMapND
from dnfpy.core.mapND import MapND
import random

class DistrMap(MapND):
        def __init__(self,name,size,dim=1,dt=1.,wrap=True,intensity=0,number=0,width=0.1,
                     ):
                super(DistrMap,self).__init__(name,size,dim=dim,dt=dt,wrap=wrap,
                                intensity=intensity,number=number,width=width,
                                              )

        def _compute(self,size,wrap,intensity,width,number,dtype,dim):
                self._data = np.zeros((size),dtype=dtype)
                for i in range(number):
                        center = np.random.random(dim)*size
                        distrI = utils.gaussNd(size,wrap,intensity,width,center)
                        self._data = self._data + distrI



