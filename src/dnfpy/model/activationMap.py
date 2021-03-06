import numpy as np
from dnfpy.core.map2D import Map2D

class ActivationMap(Map2D):
    def __init__(self,name,size,dt=0.1,type='step',th=0.75,beta=8,**kwargs):
        super(ActivationMap,self).__init__(name,
            size=size,dt=dt,type=type,th=th,beta=beta,**kwargs)

    def _compute(self,type,field,th,dtype,beta):
        #if 'cnft' in model:
        if type ==  'step':
            self._data = np.where(field > th,dtype(1),dtype(0))
        elif  type == 'sigm' :
            self._data = 1/(1+np.exp(-beta*(field-th)))
        elif type== 'id':
            self._data = np.maximum(field,dtype(0))
        else:
            raise NameError(" Invalid activation type option : %s. It should be 'sigm' or 'step' or 'id' " % type)
