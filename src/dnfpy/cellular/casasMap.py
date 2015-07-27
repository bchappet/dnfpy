from dnfpy.core.map2D import Map2D
import numpy as np
from numba import jit

size = 2000
N =np.zeros((size,size),dtype=np.bool_)
S =np.zeros((size,size),dtype=np.bool_)
E =np.zeros((size,size),dtype=np.bool_)
W =np.zeros((size,size),dtype=np.bool_)

class CasasMap(Map2D):
        def __init__(self,name,size,dt=0.1,sizeStream=2000,pSpike=0.01,
                 precisionProba=31,
                 iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.4,alpha=10,
                 iExc_=1.,iInh_=1.,pInh_=0.,pExc_=0.,reproductible=True,
                 nstep=1,shift=5,nbSharedBit=31,
                 **kwargs):
            super(CasasMap,self).__init__(name,size,dt=dt,
                sizeStream=sizeStream,pSpike=pSpike,
                precisionProba=precisionProba,nstep=nstep,
                iExc=iExc,iInh=iInh,pExc=pExc,pInh=pInh,alpha=alpha,
                iExc_=iExc_,iInh_=iInh_,pInh_=pInh_,pExc_=pExc_,
                reproductible=reproductible,
                shift=shift,nbSharedBit=nbSharedBit,
                                                      **kwargs)
        #@jit
        def __str__(self):
            size = self.getArg('size')
            ret = str(self._data)
            return ret




        def reset(self):
            super(CasasMap,self).reset()
            size = self._init_kwargs['size']



        def _compute(self,activation,size):
            print activation
            self.computeMap(activation,size)

        @jit
        def computeMap(self,activation,size):
            for i in range(size):
                for j in range(size):
                    N[...] = False
                    S[...] = False
                    E[...] = False
                    W[...] = False
                    
                    


