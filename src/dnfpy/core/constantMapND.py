from dnfpy.core.mapND import MapND
import numpy as np

class ConstantMapND(MapND):
    def __init__(self,name,size,value,**kwargs):
        MapND.__init__(self,name,size,dim=len(value.shape),dt=1e10,value=value,**kwargs)

    def _compute(self,value):
        self._data = value

    def setData(self,data):
        self.setParams(value=data)
        self.compute()

    def reset(self):
        super(ConstantMapND,self).reset()
        self._data = self._init_kwargs['value']
