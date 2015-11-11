import numpy as np
from dnfpy.core.mapND import MapND




class ActivationMapND(MapND):
    def __init__(self,name,size,dim=1,dt=0.1,type='step',th=0.75,beta=8,**kwargs):
        super(ActivationMapND,self).__init__(name,
            size=size,dim=dim,dt=dt,type=type,th=th,beta=beta,**kwargs)

    def _compute(self,type,field,th,dtype,beta):
            self._data =  ActivationMapND.activation(field,type,th,dtype,beta)


    @staticmethod
    def activation(data,type,th,dtype,beta):
        if type ==  'step':
            return np.where(data > th,dtype(1),dtype(0))
        elif  type == 'sigm' :
            return 1/(1+np.exp(-beta*(data-th)))
        elif type== 'id':
            return np.maximum(data,dtype(0))
        else:
            raise NameError(" Invalid activation type option : %s. It should be 'sigm' or 'step' or 'id' " % type)

