import numpy as np
import cv2
import random
from dnfpy.cellular.cellularMap import CellularMap
import dnfpy.core.utils as utils

def sig(X):
        """Return boolean array (there is a particule) transformed in integer"""
        return (X > 0).astype(np.int)

def res(A,psi,X):
        #psi > 0  -> X
        #psi < 0  -> 0
        #psi 0 -> A
        res = np.copy(A)
        res[psi < 0] = 0
        
        coord = psi > 0
        res[coord] = X[coord]

        

        
        #right =   np.where(psiX > 0,X,psiX)
        #tot = np.where(psiX < 0,0,A+right)
        return res


class Hpp(CellularMap):
    def __init__(self,name,size,dt=0.1,nbCol=4,colTh=0.2,**kwargs):
        self.nbDir = 4
        super(Hpp,self).__init__(name,size,dt=dt,
                                         nbCol=nbCol,colTh=colTh,**kwargs)

    def _compute(self):
            self.compute()

    @profile
    def compute(self):
        X = np.copy(self._data)

        #v 0 -> (1,0) -> n
        #v 1 -> (0,1) -> e
        #v 2 -> (-1,0) ->s
        #v 3 -> (0,-1) ->w
        pm1_0 = cv2.copyMakeBorder(self._data[2:,1:-1,0],1,1,1,1,cv2.BORDER_WRAP)
        qm1_1 = cv2.copyMakeBorder(self._data[1:-1,0:-2,1],1,1,1,1,cv2.BORDER_WRAP)
        p1_2 = cv2.copyMakeBorder(self._data[0:-2,1:-1,2],1,1,1,1,cv2.BORDER_WRAP)
        q1_3 = cv2.copyMakeBorder(self._data[1:-1,2:,3],1,1,1,1,cv2.BORDER_WRAP)

        spm1_0 = sig(pm1_0)
        sqm1_1 = sig(qm1_1)
        sp1_2 = sig(p1_2)
        sq1_3 = sig(q1_3)

        #colision rule
        psiX = ((spm1_0 * sp1_2 * (1-sqm1_1) * (1-sq1_3))
         - ((1-spm1_0) * (1-sp1_2) * sqm1_1 * sq1_3))
        psiX &= self.obs

        #print psiX
        #Update of the map
        x = self._data

        (randomHN,randomHS) = self.makeRandom(qm1_1,q1_3)
        (randomVE,randomVW) = self.makeRandom(p1_2,pm1_0)
        
        x[:,:,0] =  res(pm1_0,-psiX,randomHN)
        x[:,:,1] =  res(qm1_1,psiX,randomVE)
        x[:,:,2] =  res(p1_2,-psiX,randomHS)
        x[:,:,3] =  res(q1_3,psiX,randomVW)

        #self.applyObstacle(x)
        print "after",np.sum(X)

    def applyObstacle(self,x):
        #if in obstacle we invert the direction
        nbEqual = np.sum(x[:,:,0][self.obs] == x[:,:,2][self.obs])
        print "nbEqual",nbEqual

        tmp = x[:,:,0][self.obs]  
        x[:,:,0][self.obs] = x[:,:,2][self.obs]
        x[:,:,2][self.obs] = tmp

        tmp = x[:,:,1][self.obs]  
        x[:,:,1][self.obs] = x[:,:,3][self.obs]
        x[:,:,3][self.obs] = tmp


        #print "X : "
        #print X

    @profile
    def makeRandom(self,X,Y):
            """Return two array with a selection of one or the other array"""

            #rand = np.random.randint(0,2,X.shape).astype(bool)
            #res1 = np.where(rand,X,Y)
            #res2 = np.where(rand,Y,X)
            #return (res1,res2)
            return (X,Y)



    def init(self,size):
        X= np.zeros((size,size,self.nbDir),dtype=np.int)
        #Y obstacles
        Y= np.zeros((size,size),dtype=np.bool_)
        Y[0:,0] = True
        Y[0,0:] = True
        Y[-1,0:] = True
        Y[0:,-1] = True
        r=size/20
        Y[size/2-r:size/2+r,size/2-r:size/2+r] = True
        self.obs = Y


        self.init2(size,X)
        X[Y] = 0
        return X

    def init2(self,size,X):
       X[5,4,1] = 1
       #X[6,5,0] = 1
       X[5,6,3] = 2
       #X[4,5,2] = 1
       X+= (np.random.randint(0,2,(size,size,self.nbDir)))

    def getData(self):
            exc =  np.sum(self._data==1,axis=2)
            inh =  np.sum(self._data==2,axis=2)
            return exc - inh
            #return np.sum(self._data,axis=2)


    def onClick(self,x,y):
        X = self._data
        size = self.getArg('size')
        gauss = utils.gauss2d(size,True,1,size/10.,x,y)
        spot = np.where(gauss > 0.5,1,0)
        spot4 = np.dstack([spot]*4)
        X |= spot4


