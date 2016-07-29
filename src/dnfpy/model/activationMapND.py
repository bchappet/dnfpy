import numpy as np
from dnfpy.core.mapND import MapND




class ActivationMap(MapND):
    def __init__(self,name,size,dim=1,dt=0.1,type='step',th=0.75,beta=8,
                errorProb=0.0,errorType='none',
                **kwargs):
        super(ActivationMap,self).__init__(name,
            size=size,dim=dim,dt=dt,type=type,th=th,beta=beta,
            errorProb=errorProb,errorType=errorType,
            **kwargs)

        shape = (size,)*dim
        if "permanent" in errorType:
            self.errorMap = np.random.random(shape) <= errorProb
        else:
            self.errorMap = np.zeros(shape)



    def _compute(self,type,field,th,dtype,beta,size,errorProb,errorType):
            self._data =  ActivationMap.activation(field,type,th,dtype,beta)
            if errorType == 'none':
                pass
            elif errorType == 'permanent_high':
                self._data[self.errorMap] = 1
            elif errorType == 'permanent_low':
                self._data[self.errorMap] = 0




    @staticmethod
    def activation(data,type,th,dtype,beta):
        if type ==  'step':
            return np.where(data > th,dtype(1),dtype(0))
        elif  type == 'sigm' :
            return 1/(1+np.exp(-beta*(data-th)))
        elif type== 'id':
            return np.maximum(data,dtype(0))
        elif type == 'cnn': #cellular neural network activation function
            return 0.5*(np.abs(data+1) - np.abs(data -1 ))
        else:
            raise NameError(" Invalid activation type option : %s. It should be 'sigm' or 'step' or 'id' " % type)

