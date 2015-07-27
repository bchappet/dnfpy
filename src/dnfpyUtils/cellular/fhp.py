import numpy as np
import math
from dnfpy.core.map2D import Map2D
import scipy as sp
import cv2
import random
from dnfpy.cellular.cellularMap import CellularMap
import dnfpy.core.utils as utils
from threading import Lock


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



class Fhp(CellularMap):
    def __init__(self,name,size,sizeX=500,sizeY=500,dt=0.1,nbCol=4,colTh=0.2,wrap=True,**kwargs):
        self.nbDir = 6
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.dpc = 0.5 #density per cell
        super(Fhp,self).__init__(name,sizeX,dt=dt,sizeX=sizeX,sizeY=sizeY,
                                         nbCol=nbCol,colTh=colTh,wrap=wrap,**kwargs)
        self.lock = Lock()


    def _compute(self,sizeX,sizeY,wrap):
            self.compute(sizeX,sizeY,wrap)

    def compute(self,sizeX,sizeY,wrap):
        self.lock.acquire()
        #wrap
        if wrap:
                border = cv2.BORDER_WRAP
        else:
                border = cv2.BORDER_CONSTANT

        X = self._data.astype(np.uint8)
        xa = cv2.copyMakeBorder(X[:,:,0],1,1,1,1,border,0).astype(np.bool_)
        xb = cv2.copyMakeBorder(X[:,:,1],1,1,1,1,border,0).astype(np.bool_)
        xc = cv2.copyMakeBorder(X[:,:,2],1,1,1,1,border,0).astype(np.bool_)
        xd = cv2.copyMakeBorder(X[:,:,3],1,1,1,1,border,0).astype(np.bool_)
        xe = cv2.copyMakeBorder(X[:,:,4],1,1,1,1,border,0).astype(np.bool_)
        xf = cv2.copyMakeBorder(X[:,:,5],1,1,1,1,border,0).astype(np.bool_)

        a = np.copy(xa[1:-1,1:-1])
        b = np.copy(xb[1:-1,1:-1])
        d = np.copy(xd[1:-1,1:-1])
        e = np.copy(xe[1:-1,1:-1])
    
        #propagation on the same row
        c = np.copy(xc[1:-1,0:-2])
        f = np.copy(xf[1:-1,2:  ])

        #propagation toward different row
        #black row(even) receive from white row(odd)
        a[1::2,:] = xa[3:  :2 , 2:   ]
        b[1::2,:] = xb[3:  :2 , 1:-1 ]
        d[1::2,:] = xd[1:-2:2 , 1:-1 ]
        e[1::2,:] = xe[1:-2:2 , 2:   ]

        #And white row receive form black row
        a[::2,:] = xa[2:  :2 , 1:-1 ]
        b[::2,:] = xb[2:  :2 , 0:-2 ]
        d[::2,:] = xd[0:-2:2 , 0:-2 ]
        e[::2,:] = xe[0:-2:2 , 1:-1 ]


        #solve collisions

        #two-body collision
        #<-> particles in cells a (b,c) and d (e,f)
        #no particles in other cells
        #<-> db1 (db2,db3) = 1
        db1 = (a&d&~(b|c|e|f))
        db2 = (b&e&~(a|c|d|f))
        db3 = (c&f&~(a|b|d|e))


        # three-body collision <-> 0,1 (bits) alternating
        #<-> triple = 1 */
        triple = (a^b)&(b^c)&(c^d)&(d^e)&(e^f)

        #change a and d 
        #   <-> 
        #   three-body  collision   triple=1
        #or two-body collision db1 = 1
        #or two-body collision db2=1 and xi=1 (-rotation)
        #or two-body collision db3=1 and noxi=1 (+rotation)
        #   <-> chad=1
        xi = np.random.randint(0,2,(self.sizeY,self.sizeX)).astype(np.bool_);  #/* random bits */
        noxi = ~xi;

        obs = ~self.nsb
        obsa = a & obs
        obsb = b & obs
        obsc = c & obs
        obsd = d & obs
        obse = e & obs
        obsf = f & obs


        cha = ((triple | db1 |(xi & db2) | (noxi & db3)) & self.nsb) | (obs & (a | d))
        chd = ((triple | db1 |(xi & db2) | (noxi & db3)) & self.nsb) | (obs & (d | a))

        chb = ((triple | db2 |(xi & db3) | (noxi & db1)) & self.nsb) | (obs & (b | e))
        che = ((triple | db2 |(xi & db3) | (noxi & db1)) & self.nsb) | (obs & (e | b))

        chc = ((triple | db3 |(xi & db1) | (noxi & db2)) & self.nsb) | (obs & (c | f))
        chf = ((triple | db3 |(xi & db1) | (noxi & db2)) & self.nsb) | (obs & (f | c))


        # change: a = a ^ chad
        X[:,:,0] = a^cha;
        X[:,:,1] = b^chb;
        X[:,:,2] = c^chc;
        X[:,:,3] = d^chd;
        X[:,:,4] = e^che;
        X[:,:,5] = f^chf;
        # collision finished */


        #Bondaries condition
       # X[:,0,:] = np.random.randint(0,2,(size,6)).astype(np.bool_)
       # X[:,-1,:] = False

        
        self._data = X
        #print np.sum(X)
        self.lock.release()

    def init(self,size):
        X= np.zeros((self.sizeY,self.sizeX,self.nbDir),dtype=np.bool)
        self.nsb = np.ones((self.sizeY,self.sizeX),dtype=np.bool) #not solid blocks
        l = self.sizeY/10
        L = self.sizeX/40
        #self.nsb[size/4-l:size/4+l,size/4-2] = False

#        self.nsb[0,:] = False
#        self.nsb[-1,:] = False
#        self.nsb[size/2-l:size/2+l,size/2-L:size/2+L] = False

        self.init2(self.sizeX,self.sizeY,X)
        X[~self.nsb] = 0
        return X

    def init2(self,sizeX,sizeY,X):
       X[self.sizeY/2,self.sizeX/2-1,2] = True
       X[self.sizeY/2,self.sizeX/2+1,5] = True
       self.ro = 2.1
       X += (np.random.random((self.sizeY,self.sizeX,6)) < self.dpc)


       u = self.celerity(X)
       print("u : %s,%s"%(np.mean(u[0,:]),np.mean(u[1,:])))


      
    def celerity(self,X):
       rouX = 0
       rouY = 0
       for i in range(0,6):
           j=i-1
           rouX += X[:,:,i] * math.cos(math.pi/3*j)
           rouY += X[:,:,i] * math.sin(math.pi/3*j)
       rou = np.dstack((rouX,rouY))
       u =  rou/self.ro
       return u





       

       X[:,:,2] = True

    def getViewData(self):
        data = np.sum(self._data,axis=2)
        data += (~self.nsb).astype(np.uint8) * 1
        return data

    def getArrays(self):
            return []



    def onClick(self,x,y):
        self.lock.acquire()
        size = self.getArg('size')
        gauss = utils.gauss2d(size,True,1,size/20.,float(x)/size*self.sizeX,float(y)/size*self.sizeY)
        gauss = gauss[0:self.sizeY,0:self.sizeX]
        spot = np.where(gauss > 0.5,1,0).astype(np.bool_)
        spot *= (np.random.random((self.sizeY,self.sizeX)) < self.dpc)
        spot4 = np.dstack([spot]*6)
        self._data |= spot4
        self.lock.release()


