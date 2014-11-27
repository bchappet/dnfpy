from dnfpy.core.map2D import Map2D
import numpy as np

class FieldMap(Map2D):
    def _compute(self,model,lat,aff,dt,tau,h,th):

        if model == 'cnft':
            self._data = self._data + dt/tau*(-self._data + h + aff + lat)
        elif model == 'spike':
            self._data = np.where(self._data > th,0.,self._data) # if x > th => x = 0
            self._data = self._data + dt/tau*(-self._data + h + aff ) +  1/tau*lat
        else:
            print "Invalid model option : " + model

