# -*- coding: utf-8 -*-
'''
Reaction Diffusion : Gray-Scott model

References:
----------
Complex Patterns in a Simple System
John E. Pearson, Science 261, 5118, 189-192, 1993.


'''
import numpy as np
from dnfpy.cellular.cellularMap import CellularMap
import dnfpy.core.utils as utils
from dnfpy.model.multiLayerMap import MultiLayerMap


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



class GrayScott2(CellularMap,MultiLayerMap):
    def __init__(self,name,size,dt=0.1,Du=0.16,Dv=0.08,F=0.035,k=0.065,nbPlayer=2,**kwargs):
        super(GrayScott2,self).__init__(name=name,size=size,dt=dt,Du=Du,Dv=Dv,F=F,k=k,nbPlayer=nbPlayer,**kwargs)


    def init(self,size):

        nbPlayer = self._init_kwargs['nbPlayer']
        self.U = np.zeros((size+2,size+2))
        self.V = np.zeros((size+2,size+2,nbPlayer))
        self.init2(size+2,nbPlayer)


        return self.V

    def init2(self,size,nbPlayer):
        r = 20
        self.U[...] = 1.0
        self.U[size/2-r:size/2+r,size/2-r:size/2+r] = 0.50
        self.V[size/2-r:size/2+r,size/2-r:size/2+r,:] = 0.25
        self.U += 0.05*np.random.random((size,size))
        self.V += 0.05*np.random.random((size,size,nbPlayer))



    def getData(self):
        return  self.V


    def _compute(self,Du,Dv,F,k):
        u,v = self.U[1:-1,1:-1], self.V[1:-1,1:-1,:]

        Lu = (                 self.U[0:-2,1:-1] +
            self.U[1:-1,0:-2] - 4*self.U[1:-1,1:-1] + self.U[1:-1,2:] +
                            self.U[2:  ,1:-1] )

        Lv = (                 self.V[0:-2,1:-1,:] +
              self.V[1:-1,0:-2,:] - 4*self.V[1:-1,1:-1,:] + self.V[1:-1,2:,:] +
                                self.V[2:  ,1:-1,:] )

        sumV = np.sum(v,axis=2)
        uvv = u*sumV*sumV
        u += (Du*Lu - uvv +  F   *(1-u))

        sumLv = np.sum(Lv,axis=2)
        maxCoords = self.getMaxCoords(v)
        v[maxCoords] += (Dv*sumLv + uvv - (F+k)*sumV    )

    def getMaxCoords(self,v):
        rang = range(v.shape[0])
        grid = np.meshgrid(rang,rang)
        coords3 = np.argmax(v,axis=2)
        coords = (grid[1],grid[0],coords3)
        return coords



    def onClick(self,x,y):
        size = self.getArg('size') + 2
        self.V[:,:,1] += utils.gauss2d(size,False,0.5,10,x,y)
        #U += utils.gauss2d(size,False,0.5,10,x,y)
