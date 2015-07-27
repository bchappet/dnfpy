# -*- coding: utf-8 -*-
'''
Reaction Diffusion : Gray-Scott model

References:
----------
Complex Patterns in a Simple System
John E. Pearson, Science 261, 5118, 189-192, 1993.


'''
import numpy as np
import dnfpy.core.utils as utils
from dnfpy.model.multiLayerMapAlive import MultiLayerMapAlive


# Parameters from http://www.aliensaint.com/uo/java/rd/
# -----------------------------------------------------
# size  = 200
# Du, Dv, F, k = 0.16, 0.08, 0.035, 0.065 # Bacteria 1
# Du, Dv, F, k = 0.14, 0.06, 0.035, 0.065 # Bacteria 2
# Du, Dv, F, k = 0.16, 0.08, 0.060, 0.062 # Coral
# Du, Dv, F, k = 0.19, 0.05, 0.060, 0.062 # Fingerprint
# Du, Dv, F, k = 0.10, 0.10, 0.018, 0.050 # Spirals
# Du, Dv, F, k = 0.12, 0.08, 0.020, 0.050 # Spirals Dense
# Du, Dv, F, k = 0.10, 0.16, 0.020, 0.050 # Spirals Fast
# Du, Dv, F, k = 0.16, 0.08, 0.020, 0.055 # Unstable
# Du, Dv, F, k = 0.16, 0.08, 0.050, 0.065 # Worms 1
# Du, Dv, F, k = 0.16, 0.08, 0.054, 0.063 # Worms 2
# Du, Dv, F, k = 0.16, 0.08, 0.035, 0.060 # Zebrafish

#!python main.py ModelCellular 200 0.2 "{'model':'GrayScott','Du':0.16,'Dv':0.08,'F':0.035,'k':0.06}"#zebrafish
#!python main.py ModelCellular 200 0.2 "{'model':'GrayScott','Du':0.1,'Dv':0.16,'F':0.020,'k':0.05}"



class GrayScott4(MultiLayerMapAlive):
    def __init__(self,name,size,dt=0.1,Du=0.16,Dv=0.08,F=0.035,k=0.065,nbCol=4,
                 colTh = 0.2,**kwargs):
        super(GrayScott4,self).__init__(name=name,size=size,dt=dt,Du=Du,Dv=Dv,F=F,k=k,
                                        nbCol=nbCol,colTh=colTh,**kwargs)


    def init(self,size):
        super(GrayScott4,self).init(size)

        X = np.zeros((size,size), [('U', np.double), ('V', np.double)])
        U,V = X['U'], X['V']
        #u,v = U[1:-1,1:-1], V[1:-1,1:-1]

        U[...] = 1.0
        U += 0.05*np.random.random((size,size))
        V += 0.05*np.random.random((size,size))
        self.init2(size,U,V)
        return X


    def init2(self,size,U,V):
        r = 20
        U[size/2-r:size/2+r,size/2-r:size/2+r] = 0.50
        V[size/2-r:size/2+r,size/2-r:size/2+r] = 0.25
        #self.colors[size/2-r:size/2+r,size/2-r:size/2+r,0] = 1

    def getData(self):
        return  self._data['V']


    def _compute(self,Du,Dv,F,k):
        self.compute(Du,Dv,F,k)

    @profile
    def compute(self,Du,Dv,F,k):
        U,V = self._data['U'], self._data['V']
        u,v = U[1:-1,1:-1], V[1:-1,1:-1]

        Lu = (                 U[0:-2,1:-1] +
            U[1:-1,0:-2] - 4*U[1:-1,1:-1] + U[1:-1,2:] +
                            U[2:  ,1:-1] )

        Lv = (                 V[0:-2,1:-1] +
            V[1:-1,0:-2] - 4*V[1:-1,1:-1] + V[1:-1,2:] +
                            V[2:  ,1:-1] )

        self.updateColors(V)
        uvv = u*v*v
        u += (Du*Lu - uvv +  F   *(1-u))
        v += (Dv*Lv + uvv - (F+k)*v    )
        self.eraseColorThreshold(V)


    def onClick(self,x,y):
        V = self._data['V']
        size = self.getArg('size')
        gauss = utils.gauss2d(size,False,0.5,10,x,y)
        V += gauss
        self.colorise(gauss,True)


