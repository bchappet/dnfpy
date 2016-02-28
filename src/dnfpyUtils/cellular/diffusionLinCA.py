# -*- coding: utf-8 -*-
'''

'''
import numpy as np
from dnfpy.cellular.cellularMap import CellularMap
import dnfpy.core.utils as utils



#python3 main.py --model ModelCellular --params "{'model':'DiffusionLinCA'}" --scenario None


class DiffusionLinCA(CellularMap):
    """

    m : state max (when activated)
    pt : probability of tranmiting the activation

    activation : child (boolean) if true, cell is excited
    obstacle : child (boolean) if true there is obstacle => cell is always 0
    """
    def __init__(self,name,size,pt=1.0,m=100,activation=None,obstacle=None,**kwargs):
        super().__init__(name=name,size=size,pt=pt,m=m,activation=activation,obstacle=obstacle,**kwargs)

    def init(self,size):
        return np.zeros((size,size),dtype=np.uint8)




    def _compute(self,size,pt,m,activation,obstacle):
        X = self._data

        N = X[0:-2,1:-1]  
        W = X[1:-1,0:-2] 
        E = X[1:-1,2:]
        S = X[2:  ,1:-1] 

        x = X[1:-1,1:-1]

        #random = np.random.random((size-2,size-2)) < pt

        getN = (N > 0) & ((N != x+1) & (N != x-1))
        getE = (E > 0) & ((E != x+1) & (E != x-1)) & (E != N)
        getW = (W > 0) & ((W != x+1) & (W != x-1)) & (W != N) & (W != E)
        getS = (S > 0) & ((S != x+1) & (S != x-1)) & (S != N) & (S != E) & (S != W)



        x[getN] += N[getN] - 1
        x[getE] += E[getE] - 1
        x[getW] += W[getW] - 1
        x[getS] += S[getS] - 1

        #x[decrement] -= 1

        if activation:
            X[activation & (X==0)] = m

        if obstacle:
            X[obstacle]   = 0



    def onClick(self,x,y):
        size = self.getArg('size') 
        m = self.getArg("m")
        self._data[y,x] = m
        #U += utils.gauss2d(size,False,0.5,10,x,y)
