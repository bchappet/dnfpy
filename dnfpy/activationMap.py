import numpy as np
from map2D import Map2D

class ActivationMap(Map2D):
    def compute(self):
        super(ActivationMap,self).compute()
        model = self.globalRealParams['model']
        field = self.children['field'].getData()
        if model == 'cnft':
            self.data = np.maximum(field,0)
        elif model == 'spike':
            th = self.globalRealParams['threshold']
            self.data = np.where(field > th,1.,0.)
        else:
            print " Invalid model option : %s" % self.globalRealParams['model']
