import numpy as np
from dnfpy.core.map2D import Map2D

class ActivationMap(Map2D):
    def __init__(self,name,size,dt=0.1,model='cnft',th=0.75,dtype=np.float32,**kwargs):
        super(ActivationMap,self).__init__(name,
            size=size,dt=dt,model=model,th=th,dtype=dtype,**kwargs)
    def _compute(self,model,field,th,dtype):
        if model == 'cnft':
            self._data = np.maximum(field,dtype(0))
        elif model == 'spike':
            self._data = np.where(field > th,dtype(1),dtype(0))
        else:
            print " Invalid model option : %s" % model
