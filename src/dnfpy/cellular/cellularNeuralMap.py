from dnfpy.core.map2D import Map2D
import numpy as np


class CellularNeuralMap(Map2D):
    """
    A cellular neural map is a map which mainly use cellar computation to update its
    potentials.
    It expects a cellular automata in input and a delta potential $dp$ which
    will be added to its potential every time the cellular automata is state is 
    "activationState"

    
    """
    def __init__(self,name,size,dt=0.1,da=1,di=1,activationState=1,**kwargs):
        super(CellularNeuralMap,self).__init__(name,size,dt=dt,da=da,di=di,
                        activationState=activationState,**kwargs)


    def _compute(self,actMap,inhMap,activationState,da,di):
        self._data[actMap == activationState] += da
        self._data[inhMap == activationState] += di

    def resetLat(self):
        size = self.getArg('size')
        dtype = self.getArg('dtype')
        self._data = np.zeros((size,size),dtype=dtype)
        self.getArg('actMap')[...] = 0
        self.getArg('inhMap')[...] = 0





from dnfpy.cellular.cellularMap import CellularMap
from dnfpy.core.map2D import Map2D

class BlockRotationDiffusion(Map2D):
        def __init__(self,name,size,dt=0.1,wrap=False,dtype=np.bool_,p=0.5,**kwargs):
                super(BlockRotationDiffusion,self).__init__(name,size,dt=dt,wrap=wrap,dtype=dtype,p=p,**kwargs)

                self.mask = np.ones((size,size),dtype=np.bool_)
                self.mask[1:-1,1:-1] = False

        def _compute(self,activation,p):
            self._data[activation] = True
            self._data = self.margolusStep(self._data,0,p)
            self._data = self.margolusStep(self._data,1,p)


        def margolusStep(self,X,s,p):
            """
            s is the shift in margolus 2 block computations s \in {1,0}
            """
            Y = np.zeros_like(X)
            #rot + pi/2
            rand = np.random.random((X.shape[0]//2-s,X.shape[1]//2-s)) < p 
            #rot - pi/2
            norand = ~rand

            #print rand.shape, X[s+1:  :2,s+0:-1:2].shape

            Y[s+0:-1:2,s+0:-1:2] = (rand & X[s+1:  :2,s+0:-1:2]) | (norand & X[s+0:-1:2,s+1:  :2])
            Y[s+0:-1:2,s+1:  :2] = (rand & X[s+0:-1:2,s+0:-1:2]) | (norand & X[s+1:  :2,s+1:  :2])
            Y[s+1:  :2,s+1:  :2] = (rand & X[s+0:-1:2,s+1:  :2]) | (norand & X[s+1:  :2,s+0:-1:2])
            Y[s+1:  :2,s+0:-1:2] = (rand & X[s+1:  :2,s+1:  :2]) | (norand & X[s+0:-1:2,s+0:-1:2])
            Y[self.mask] = False

            return Y

                











class ExplorationCA(Map2D):
        def __init__(self,name,size,dt=0.1,wrap=False,lut=[]*(2**6),dtype=np.bool_,**kwargs):
                super(ExplorationCA,self).__init__(name,size,dt=dt,wrap=wrap,lut=lut,dtype=dtype,**kwargs)

        def _compute(self,activation,lut):
            X = self._data
            #N = (X[0:-2,0:-2] + X[0:-2,1:-1] + X[0:-2,2:] +
            #     X[1:-1,0:-2]                + X[1:-1,2:] +
            #     X[2:  ,0:-2] + X[2:  ,1:-1] + X[2:  ,2:])
            x = X[1:-1,1:-1]
            N = X[0:-2,1:-1]
            S = X[2:  ,1:-1]
            E = X[1:-1,2:  ]
            W = X[1:-1,0:-2]
            a = activation[1:-1,1:-1].astype(np.bool_)

            binary = x << 5 | N << 4 | S << 3 | E << 2 | W << 1 | a
            self._data[1:-1,1:-1] = np.take(lut,binary)






