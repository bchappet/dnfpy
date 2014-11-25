import numpy as np
from dnfpy.core.map2D import Map2D

class ActivationMap(Map2D):
    def _compute(self,model,field,th):
        if model == 'cnft':
            self._data = np.maximum(field,0)
        elif model == 'spike':
            self._data = np.where(field > th,1.,0.)
        else:
            print " Invalid model option : %s" % model
