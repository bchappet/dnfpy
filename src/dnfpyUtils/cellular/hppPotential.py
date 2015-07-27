import numpy as np
from dnfpy.model.inputMap import InputMap
from dnfpy.core.map2D import Map2D
import scipy as sp
import cv2
import random
from dnfpy.cellular.cellularMap import CellularMap
import dnfpy.core.utils as utils
from threading import Lock


class ActMap(Map2D):
    """Activation map: is active when a kernel potential is higher than a threshold
    """
    def __init__(self,name,size,dt=0.1,th=3.5,sizeAct=5,**kwargs):
        super(ActMap,self).__init__(name,size,dt=dt,th=th,dtype=np.bool_,
                sizeAct=sizeAct,**kwargs)

    def _compute(self,pot,th,sizeAct):
        res = np.where(pot > th,True,False).astype(np.uint8)
        kernel = np.ones((sizeAct,sizeAct),dtype=np.uint8)
        conv = cv2.filter2D(res,-1,cv2.flip(kernel,-1),anchor=(-1,-1))
        self._data = conv > 0


class HppSum(Map2D):
        """
        HppExc - HppInh
        """
        def __init__(self,name,size,dt=0.1,**kwargs):
                super(HppSum,self).__init__(name,size,dt=dt,dtype=np.float,**kwargs)

        def _compute(self,hppExc,hppInh):
                self._data = np.sum(hppExc,axis=2) - np.sum(hppInh,axis=2)
                


class HppPotential(CellularMap):
    """
    Compte the potential of the neurons
    alpha is the quantity to add or remove to the potential depending on the number of parts
    """
    def __init__(self,name,size,dt=0.1,alpha=0.1,th=2.,**kwargs):
        super(HppPotential,self).__init__(name,size,dt=dt,dtype=np.float,alpha=alpha,th=th,**kwargs)


        self.aff = InputMap("Inputs",size,dt=1e10)

        self.activationExc = ActMap("actExc",size,dt=dt,th=th,sizeAct=5)
        self.activationExc.addChildren(pot=self)
        self.activationInh = ActMap("actInh",size,dt=dt,th=th,sizeAct=11)
        self.activationInh.addChildren(pot=self)


        self.hppExc = Hpp2("hppExc",size)
        self.hppInh = Hpp2("hppInh",size)

        self.hppExc.addChildren(activation=self.activationExc,potential=self)
        self.hppInh.addChildren(activation=self.activationInh,potential=self)

        self.sumHpp = HppSum("hppSum",size)
        self.sumHpp.addChildren(hppExc = self.hppExc,hppInh = self.hppInh)

        self.addChildren(hpp=self.sumHpp,input=self.aff)

    def _compute(self,hpp,input,alpha,th):
        
        #reset pot on activation

        self._data = np.where(self._data > th,0.0,self._data)

        somme = hpp
        #mean = np.mean(somme)
        #kernel = np.ones((3,3),dtype=np.uint8)
        #kSum = np.sum(kernel)
        #conv = cv2.filter2D(somme,-1,cv2.flip(kernel,-1),anchor=(-1,-1))
        #print np.mean(conv)

        #self.pot = conv > (mean + 0.6)*kSum

        toAdd = np.where(somme > 0. ,alpha,-alpha)
        self._data += toAdd
        self._data += input * 0.05
        self._data = np.clip(self._data,-1,9999999)


    def getArrays(self):
        return [self.activationInh,self.sumHpp,self.hppExc,self.hppInh]

    def onClick(self,x,y):
            self.hppExc.onClick(x,y)

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
        return res



class Hpp2(CellularMap):
    def __init__(self,name,size,dt=0.1,nbCol=4,colTh=0.2,**kwargs):
        self.nbDir = 4
        super(Hpp2,self).__init__(name,size,dt=dt,
                                         nbCol=nbCol,colTh=colTh,**kwargs)
        self.lock = Lock()


    def _compute(self,activation):
            self.compute(activation)

    @profile
    def compute(self,activation):
        self.lock.acquire()

        self._data[:,:,0] |= activation
        self._data[:,:,1] |= activation
        self._data[:,:,2] |= activation
        self._data[:,:,3] |= activation


        #print("Nb part : %s"%np.sum(self._data))




        X = self._data.astype(np.uint8)
        Y = np.copy(self.obs)
        #v 0 -> (1,0) -> n
        #v 1 -> (0,1) -> e
        #v 2 -> (-1,0) ->s
        #v 3 -> (0,-1) ->w
        x0 = cv2.copyMakeBorder(X[:,:,0],1,1,1,1,cv2.BORDER_WRAP).astype(np.bool_)
        x1 = cv2.copyMakeBorder(X[:,:,1],1,1,1,1,cv2.BORDER_WRAP).astype(np.bool_)
        x2 = cv2.copyMakeBorder(X[:,:,2],1,1,1,1,cv2.BORDER_WRAP).astype(np.bool_)
        x3 = cv2.copyMakeBorder(X[:,:,3],1,1,1,1,cv2.BORDER_WRAP).astype(np.bool_)

        pm1_0 = x0[2:,1:-1]
        qm1_1 = x1[1:-1,0:-2]
        p1_2 = x2[0:-2,1:-1]
        q1_3 = x3[1:-1,2:]


        #colision rule 1 if collision
        psiX = (((pm1_0 & p1_2) & ~(qm1_1 | q1_3)) |
               (~(pm1_0 | p1_2) &  (qm1_1 & q1_3)) )
        psiX = ( psiX & (~Y))
        

        X = X.astype(np.bool_,copy = False)
        ##update of the map if collision: 1 ^ 1 -> 0
        ##If obstacle collision = 0 life goes on
        ##if obstacle: we invert the direction of part  
        #   part here: 1 ^ 1 -> 0
        #   oposite direction 0 ^ 1 -> 1
        #   other direction 0 ^ 0 -> 0
        obsVert = (Y & (pm1_0|p1_2))
        obsHori = (Y & (qm1_1|q1_3))
        X[...] = 0
        X[:,:,0] = (pm1_0 ^ psiX) ^ obsVert
        X[:,:,1] = (qm1_1 ^ psiX) ^ obsHori
        X[:,:,2] = (p1_2 ^ psiX) ^ obsVert
        X[:,:,3] = (q1_3 ^ psiX) ^ obsHori

                #print np.sum(x)
        self._data = X
        self.lock.release()

    def init(self,size):
        X= np.zeros((size,size,self.nbDir),dtype=np.bool)
        #Y obstacles
        Y= np.zeros((size,size),dtype=np.bool_)
        #Y[0:,0] = True
        #Y[0,0:] = True
        #Y[-1,0:] = True
        #Y[0:,-1] = True
        r=size/20
        #Y[size/4-4*r-r:size/4+4.5*r,size/2-r:size/2+r] = True
        #Y[size/4*3-4.5*r:size/4*3+4.5*r+r,size/2-r:size/2+r] = True
        self.obs = Y


        self.mean = 0


        self.init2(size,X)
        X[Y] = 0
        return X

    def init2(self,size,X):
       #X[5,4,1] = 1
       #X[6,5,0] = 1
       X[5,6,3] = 1
       #X[4,5,2] = 1
       #X+= (np.random.randint(0,2,(size,size,self.nbDir))).astype(np.bool_)
       r=size/20
       #X[:,0:size/2-r,:] = (np.random.random((size,size,4)) < 0.7)[:,0:size/2-r,:]
       X += (np.random.random((size,size,4)) < 0.6)

    def getViewData(self):
        data = np.sum(self._data,axis=2)
        return data


    def onClick(self,x,y):
        self.lock.acquire()
        size = self.getArg('size')
        gauss = utils.gauss2d(size,True,1,size/20.,x,y)
        spot = np.where(gauss > 0.5,1,0).astype(np.bool_)
        spot4 = np.dstack([spot]*4)
        self._data |= spot4
        self.lock.release()



