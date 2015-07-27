import numpy as np
import cv2
from dnfpy.cellular.cellularMap import CellularMap
import dnfpy.core.utils as utils
from dnfpy.core.map2D import Map2D


class HppMap(Map2D):
    def __init__(self,name,size,dt=0.1,**kwargs):
        self.nbDir = 4
        super(HppMap,self).__init__(name,size,dt=dt,**kwargs)

    def _compute(self,source):
            self.compute(source)

    

    def compute(self,source):
        #p1 = X[0:-2,1:-1] #n
        #q1 = X[1:-1,2: ] #e
        #pm1 = X[2: ,1:-1] #s
        #qm1 = X[1:-1,0:-2] #w

        pm1_0 = cv2.copyMakeBorder(self._data[2:,1:-1,0],1,1,1,1,cv2.BORDER_WRAP)
        qm1_1 = cv2.copyMakeBorder(self._data[1:-1,0:-2,1],1,1,1,1,cv2.BORDER_WRAP)
        p1_2 = cv2.copyMakeBorder(self._data[0:-2,1:-1,2],1,1,1,1,cv2.BORDER_WRAP)
        q1_3 = cv2.copyMakeBorder(self._data[1:-1,2:,3],1,1,1,1,cv2.BORDER_WRAP)

        #colision rule
        psiX = ((pm1_0 * p1_2 * (1-qm1_1) * (1-q1_3))
         - ((1-pm1_0) * (1-p1_2) * qm1_1 * q1_3))
        #psiX = 0

        #update of the map
        x = self._data
        x[...] = 0
        x[:,:,0] = pm1_0 - psix
        x[:,:,1] = qm1_1 + psix
        x[:,:,2] = p1_2 - psix
        x[:,:,3] = q1_3 + psix

        self._data[np.nonzero(source)] |= 1


    def reset(self):
        super(HppMap,self).reset()
        size =self._init_kwargs['size']
        self._data= np.zeros((size,size,self.nbDir),dtype=np.int)
        self.init2(size,self._data)

    def init2(self,size,X):
        randArr = np.random.random((size,size,self.nbDir))
        randArrInt = np.where(randArr < 0.4,1,0)
        X+= randArrInt

    def getData(self):
            return np.sum(self._data,axis=2)

    def getArrays(self):
            return []


    def onClick(self,x,y):
        X = self._data
        size = self.getArg('size')
        gauss = utils.gauss2d(size,False,1,size/10.,x,y)
        spot = np.where(gauss > 0.5,1,0)
        spot4 = np.dstack([spot]*4)
        X |= spot4


