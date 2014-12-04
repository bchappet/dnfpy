import numpy as np
from dnfpy.core.map2D import Map2D

class ActivationMap(Map2D):
    def __init__(self,size,dt=0.1,model='cnft',th=0.75,**kwargs):
        super(ActivationMap,self).__init__(
            size=size,dt=dt,model=model,th=th,**kwargs)
    def _compute(self,model,field,th):
        if model == 'cnft':
            self._data = np.maximum(field,0)
        elif model == 'spike':
            self._data = np.where(field > th,1.,0.)
        else:
            print " Invalid model option : %s" % model
