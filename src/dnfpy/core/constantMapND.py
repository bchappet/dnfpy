from dnfpy.core.mapND import MapND
import numpy as np

class ConstantMap(MapND):
    def __init__(self,name,size,value,clickVal=1,**kwargs):
        MapND.__init__(self,name,size,dim=len(value.shape),dt=1e10,value=value,clickVal=clickVal,**kwargs)

    def _compute(self,value):
        self._data = value

    def setData(self,data):
        self.setParams(value=data)
        self.compute()

    def reset(self):
        super().reset()
        self._data = self._init_kwargs['value']



    def onClick(self,x,y):
        clickVal = self.getArg('clickVal') 
        self._data[y,x] = clickVal if self._data[y,x] != clickVal else 0
