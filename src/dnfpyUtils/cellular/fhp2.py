import numpy as np
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



class Fhp2(CellularMap):
    def __init__(self,name,size,dt=0.1,nbCol=4,colTh=0.2,**kwargs):
        self.nbDir = 7
        super(Fhp2,self).__init__(name,size,dt=dt,
                                         nbCol=nbCol,colTh=colTh,**kwargs)
        self.lock = Lock()


    def _compute(self,size):
            self.compute(size)

    @profile
    def compute(self,size):
        self.lock.acquire()
        #wrap
        X = self._data.astype(np.uint8)
        xa = cv2.copyMakeBorder(X[:,:,0],1,1,1,1,cv2.BORDER_WRAP).astype(np.bool_)
        xb = cv2.copyMakeBorder(X[:,:,1],1,1,1,1,cv2.BORDER_WRAP).astype(np.bool_)
        xc = cv2.copyMakeBorder(X[:,:,2],1,1,1,1,cv2.BORDER_WRAP).astype(np.bool_)
        xd = cv2.copyMakeBorder(X[:,:,3],1,1,1,1,cv2.BORDER_WRAP).astype(np.bool_)
        xe = cv2.copyMakeBorder(X[:,:,4],1,1,1,1,cv2.BORDER_WRAP).astype(np.bool_)
        xf = cv2.copyMakeBorder(X[:,:,5],1,1,1,1,cv2.BORDER_WRAP).astype(np.bool_)
        xr = cv2.copyMakeBorder(X[:,:,6],1,1,1,1,cv2.BORDER_WRAP).astype(np.bool_)

        a = np.copy(xa[1:-1,1:-1])
        b = np.copy(xb[1:-1,1:-1])
        d = np.copy(xd[1:-1,1:-1])
        e = np.copy(xe[1:-1,1:-1])
    
        #propagation on the same row
        c = np.copy(xc[1:-1,0:-2])
        f = np.copy(xf[1:-1,2:  ])

        #resting particules are resting:
        r = np.copy(xr[1:-1,1:-1])

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


        #Rest particule and 1 particule
        ra = (r&a& ~(b|c|d|e|f))
        rb = (r&b& ~(a|c|d|e|f))
        rc = (r&c& ~(a|b|d|e|f))
        rd = (r&d& ~(a|b|c|e|f))
        re = (r&e& ~(a|b|c|d|f))
        rf = (r&f& ~(a|b|c|d|e))


        # no rest particle and 2 particles (i,i+2)
        ra2 = (f&b& ~(r|a|c|d|e))
        rb2 = (a&c& ~(r|b|d|e|f))
        rc2 = (b&d& ~(r|a|c|e|f))
        rd2 = (c&e& ~(r|a|b|d|f))
        re2 = (d&f& ~(r|a|b|c|e))
        rf2 = (e&a& ~(r|b|c|d|f))

        #change a and d 
        #   <-> 
        #   three-body  collision   triple=1
        #or two-body collision db1 = 1
        #or two-body collision db2=1 and xi=1 (-rotation)
        #or two-body collision db3=1 and noxi=1 (+rotation)
        #   <-> chad=1
        xi = np.random.randint(0,2,(size,size)).astype(np.bool_);  #/* random bits */
        noxi = ~xi;

        cha = triple | db1 |(xi & db2) | (noxi & db3) | ra | rb | rf | ra2 | rb2 | rf2 
        chd = triple | db1 |(xi & db2) | (noxi & db3) | rd | rc | re | rd2 | rc2 | re2 
        chb = triple | db2 |(xi & db3) | (noxi & db1) | rb | ra | rc | rb2 | ra2 | rc2 
        che = triple | db2 |(xi & db3) | (noxi & db1) | re | rd | rf | re2 | rd2 | rf2 
        chc = triple | db3 |(xi & db1) | (noxi & db2) | rc | rb | rd | rc2 | rb2 | rd2 
        chf = triple | db3 |(xi & db1) | (noxi & db2) | rf | ra | re | rf2 | ra2 | re2 
        chr = ra | rb | rc | rd | re | rf | ra2 | rb2 | rc2 | rd2 | re2 | rf2  


        # change: a = a ^ chad
        X[:,:,0] = a^cha
        X[:,:,1] = b^chb
        X[:,:,2] = c^chc
        X[:,:,3] = d^chd
        X[:,:,4] = e^che
        X[:,:,5] = f^chf
        X[:,:,6] = r^chr
        # collision finished */


        
        
        self._data = X
        print np.sum(X[:,:,6])

    


        self.lock.release()

    def init(self,size):
        X= np.zeros((size,size,self.nbDir),dtype=np.bool)
        self.init2(size,X)
        return X

    def init2(self,size,X):
       #X[size/2,size/2-1,2] = True
       #X[size/2,size/2+1,5] = True
       #X[size/2,size/2,6] = True
       X[:,:,6] = True
       X += (np.random.random((size,size,7)) < 0.4)
       X[:,:,6] = np.random.random((size,size)) < 0.5

    def getViewData(self):
        data = np.sum(self._data,axis=2)
        return data

    def getArrays(self):
            return []



    def onClick(self,x,y):
        self.lock.acquire()
        size = self.getArg('size')
        gauss = utils.gauss2d(size,True,1,size/20.,x,y)
        spot = np.where(gauss > 0.5,1,0).astype(np.bool_)
        spot4 = np.dstack([spot]*7)
        self._data |= spot4
        self.lock.release()


