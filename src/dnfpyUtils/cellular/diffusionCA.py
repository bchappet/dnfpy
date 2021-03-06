# -*- coding: utf-8 -*-
'''

'''
import numpy as np
from dnfpy.cellular.cellularMap import CellularMap
import dnfpy.core.utils as utils



#python3 main.py --model ModelCellular --params "{'model':'DiffusionCA'}" --scenario None


class DiffusionCA(CellularMap):
    """

    m : state max (when activated)
    pt : probability of tranmiting the activation

    activation : child (boolean) if true, cell is excited
    obstacle : child (boolean) if true there is obstacle => cell is always 0
    """
    def __init__(self,name,size,pt=1.0,m=4,activation=None,obstacle=None,**kwargs):
        super().__init__(name=name,size=size,pt=pt,m=m,activation=activation,obstacle=obstacle,**kwargs)

    def init(self,size):
        return np.zeros((size,size),dtype=np.uint8)




    def _compute(self,size,pt,m,activation,obstacle):
        X = self._data
        # Count neighbours
        M = (X == m)
        N = (M[0:-2,0:-2] | M[0:-2,1:-1] | M[0:-2,2:] |
             M[1:-1,0:-2]                | M[1:-1,2:] |
             M[2:  ,0:-2] | M[2:  ,1:-1] | M[2:  ,2:])

        x = X[1:-1,1:-1]

        random = np.random.random((size-2,size-2)) < pt
        transmission = (x == 0) & N & random #if neutral and neignbour excited, pt proba to become activated
        decrement = (x > 0) & ~transmission

        x[transmission] = m

        x[decrement] -= 1

        if activation:
            X[activation & (X==0)] = m

        if obstacle:
            X[obstacle]   = 0



    def onClick(self,x,y):
        size = self.getArg('size') 
        m = self.getArg("m")
        self._data[y,x] = m
        #U += utils.gauss2d(size,False,0.5,10,x,y)
