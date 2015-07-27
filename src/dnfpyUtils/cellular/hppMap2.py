import numpy as np
from dnfpy.cellular.cellularMap import CellularMap
import dnfpy.core.utils as utils
from dnfpy.core.map2D import Map2D

from dnfpyUtils.cellular.hppMap import HppMap

def sig(X):
        """Return boolean array (there is a particule) transformed in integer"""
        return np.where(X > 0).astype(np.int)

class HppMap2(HppMap):
    def __init__(self,name,size,dt=0.1,**kwargs):
        super(HppMap2,self).__init__(name,size,dt=dt,**kwargs)

    def _compute(self,source):
            self.compute(source)

    def compute(self,source):
        X = np.copy(self._data)

        #v 0 -> (1,0) -> n
        #v 1 -> (0,1) -> e
        #v 2 -> (-1,0) ->s
        #v 3 -> (0,-1) ->w


        p1 = X[0:-2,1:-1] #n
        q1 = X[1:-1,2: ] #e
        pm1 = X[2: ,1:-1] #s
        qm1 = X[1:-1,0:-2] #w

        sp1 = sig(X[0:-2,1:-1]) #n
        sq1 = sig(X[1:-1,2: ]) #e
        spm1 = sig(X[2: ,1:-1]) #s
        sqm1 = sig(X[1:-1,0:-2]) #w



        #colision rule
        psiX = ((spm1[:,:,0] * sp1[:,:,2] * (1-sqm1[:,:,1]) * (1-sq1[:,:,3]))
         - ((1-spm1[:,:,0]) * (1-sp1[:,:,2]) * sqm1[:,:,1] * sq1[:,:,3]))
        #psiX = 0

        #Update of the map
        x = self._data[1:-1,1:-1]
        x[...] = 0

        #TODO randomize
        x[:,:,0] = pm1[:,:,0] - psiX*qm1[:,:,1] #if theris H colision, the part. from west will go up
        x[:,:,1] = qm1[:,:,1] + psiX*p1[:,:,2] #if V collision part.from north will go east
        x[:,:,2] = p1[:,:,2] - psiX*q1[:,:,3] #if H collision, the part. from east will go down
        x[:,:,3] = q1[:,:,3] + psiX*pm1[:,:,0]#if V collision the part. from south xill go west

        self._data[np.nonzero(source)] = 2



    def getData(self):
            exc =  np.sum(self._data[np.where(self._data==1)],axis=2)
            inh =  np.sum(self._data[np.where(self._data==2)],axis=2)
            return exc - inh

    def getArrays(self):
        return []
    

    def reset(self):
        super(HppMap2,self).reset()
        size =self._init_kwargs['size']
        self._data= np.zeros((size,size,self.nbDir),dtype=np.int)
        self.init2(size,self._data)

    def init2(self,size,X):
        randArr = np.random.random((size,size,self.nbDir))
        randArrInt = np.where(randArr < 0.4,1,0)
        X+= randArrInt



    def onClick(self,x,y):
        X = self._data
        size = self.getArg('size')
        gauss = utils.gauss2d(size,False,1,size/10.,x,y)
        spot = np.where(gauss > 0.5,1,0)
        spot4 = np.dstack([spot]*4)
        X |= spot4


