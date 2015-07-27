import numpy as np
from dnfpy.core.map2D import Map2D
import scipy as sp
import cv2
import random
from dnfpy.cellular.cellularMap import CellularMap
import dnfpy.core.utils as utils
from threading import Lock
from dnfpy.core.constantMap import ConstantMap




class HppReaction(CellularMap):
    def __init__(self,name,size,dnfSize=30,dt=0.1,displayedLayer=0,rho=0.3,iExc=1.25,iInh=0.7,**kwargs):
        self.rho = rho
        self.nbDir = 4
        super(HppReaction,self).__init__(name,size,dt=dt,dnfSize=dnfSize,
                                         displayedLayer=displayedLayer,
                                         rho=rho,iExc=iExc,iInh=iInh,
                                         **kwargs)
        self.lock = Lock()

    def _onAddChildren(self,**kwargs):
         if 'activation' in kwargs:
             self.activation = kwargs['activation']


    def _compute(self,size):
            self.compute(size)

    def resetLat(self):
        pass

    @profile
    def compute(self,size):
        self.lock.acquire()

        
        #self._data[:,:,0] ^= activation
        #self._data[:,:,1] ^= activation
        #self._data[:,:,2] ^= activation
        #self._data[:,:,3] ^= activation


        #print("Nb part S : %s"%np.sum(self._data['S']))
        #print("Nb part E : %s"%np.sum(self._data['E']))
        #print("Nb part I : %s"%np.sum(self._data['I']))


        E = self._data['E'].astype(np.uint8)
        I = self._data['I'].astype(np.uint8)
        S = self._data['S'].astype(np.uint8)
        #v 0 -> (1,0) -> n
        #v 1 -> (0,1) -> e
        #v 2 -> (-1,0) ->s
        #v 3 -> (0,-1) ->w
        e0 = makeBorder(E[:,:,0])
        e1 = makeBorder(E[:,:,1])
        e2 = makeBorder(E[:,:,2])
        e3 = makeBorder(E[:,:,3])

        i0 = makeBorder(I[:,:,0])
        i1 = makeBorder(I[:,:,1])
        i2 = makeBorder(I[:,:,2])
        i3 = makeBorder(I[:,:,3])

        s0 = makeBorder(S[:,:,0])
        s1 = makeBorder(S[:,:,1])
        s2 = makeBorder(S[:,:,2])
        s3 = makeBorder(S[:,:,3])


        e_N = e0[2:,1:-1]
        e_E = e1[1:-1,0:-2]
        e_S = e2[0:-2,1:-1]
        e_W = e3[1:-1,2:]

        i_N = i0[2:,1:-1]
        i_E = i1[1:-1,0:-2]
        i_S = i2[0:-2,1:-1]
        i_W = i3[1:-1,2:]

        s_N = s0[2:,1:-1]
        s_E = s1[1:-1,0:-2]
        s_S = s2[0:-2,1:-1]
        s_W = s3[1:-1,2:]

        #Any part
        p_N = e_N | i_N | s_N
        p_E = e_E | i_E | s_E
        p_S = e_S | i_S | s_S
        p_W = e_W | i_W | s_W

        #colision rule 1 if collision for any particule
        s_col = (((s_N & s_S ) & ~(p_E | p_W)) |  (~(p_N | p_S) &  (s_E & s_W) ))
        s_col1 = ((((s_N & p_S) | (p_N & s_S)) & ~(p_E | p_W)) |
               (~(p_N | p_S) &  (((s_E & p_W)) | (p_E & s_W))) )
        s_col1 = s_col1 & (~s_col)

        e_col = (((e_N & e_S ) & ~(p_E | p_W)) |(~(p_N | p_S) &  (e_E & e_W) ))
        e_col1 = ((((e_N & p_S) | (p_N & e_S)) & ~(p_E | p_W)) |
               (~(p_N | p_S) &  (((e_E & p_W)) | (p_E & e_W))) )
        e_col1 = e_col1 & (~e_col)

        i_col = (((i_N & i_S ) & ~(p_E | p_W)) |(~(p_N | p_S) &  (i_E & i_W) ))
        i_col1 = ((((i_N & p_S) | (p_N & i_S)) & ~(p_E | p_W)) |
               (~(p_N | p_S) &  (((i_E & p_W)) | (p_E & i_W))) )
        i_col1 = i_col1 & (~i_col)
        #psiX = ( psiX & (~Y))

        colVert = (p_N & p_S) & ~(p_E | p_W)
        colHori = ~(p_N | p_S) & (p_E & p_W)
        

        E = E.astype(np.bool_,copy = False)
        I = I.astype(np.bool_,copy = False)
        S = S.astype(np.bool_,copy = False)
        ##update of the map if collision: 1 ^ 1 -> 0
        ##If obstacle collision = 0 life goes on
        ##if obstacle: we invert the direction of part  
        #   part here: 1 ^ 1 -> 0
        #   oposite direction 0 ^ 1 -> 1
        #   other direction 0 ^ 0 -> 0
        #obsVert = (Y & (p_N|p_S))
        #obsHori = (Y & (p_E|p_W))

        rand = np.random.randint(0,2,(size,size)).astype(np.bool_)
        norand = ~rand

        #print("scol",s_col.astype(np.uint8))
        #print("scol1",s_col1.astype(np.uint8))
        #print("ecol",e_col.astype(np.uint8))
        #print("ecol1",e_col1.astype(np.uint8))

        S[:,:,0] = choice(size,s_N,s_col,s_col1,rand,colVert)
        S[:,:,1] = choice(size,s_E,s_col,s_col1,rand,colHori)
        S[:,:,2] = choice(size,s_S,s_col,s_col1,norand,colVert)
        S[:,:,3] = choice(size,s_W,s_col,s_col1,norand,colHori)


        E[:,:,0] = choice(size,e_N,e_col,e_col1,norand,colVert)
        E[:,:,1] = choice(size,e_E,e_col,e_col1,norand,colHori)
        E[:,:,2] = choice(size,e_S,e_col,e_col1,rand,colVert)
        E[:,:,3] = choice(size,e_W,e_col,e_col1,rand,colHori)


        I[:,:,0] = choice(size,i_N,i_col,i_col1,norand,colVert)
        I[:,:,1] = choice(size,i_E,i_col,i_col1,norand,colHori)
        I[:,:,2] = choice(size,i_S,i_col,i_col1,rand,colVert)
        I[:,:,3] = choice(size,i_W,i_col,i_col1,rand,colHori)

        self.reaction(S,E,I,rand,self.activation.getData())



        #print np.sum(x)
        self._data['S'] = S
        self._data['E'] = E
        self._data['I'] = I

        self.lock.release()

    @profile
    def reaction(self,S,E,I,R,A):
        totS = np.sum(S,axis=2) 
        totE = np.sum(E,axis=2)
        totI = np.sum(I,axis=2)
        tot = totS + totE + totI

        #A (ext) -> 4E
        E[A] = True
        e = E[1:-1]
        e[A[2:,1:-1] | A[0:-2,1:-1] | A[1:-1,2:] | A[1:-1,0:-2]] =True


       # E[(totE>3)&R] = True


        #E -> I (rate 4*(\rho **3)*0.5
        rec1 = (tot) > 2
        print('totS',totS)
        I[rec1] |= E[rec1]
        E[rec1] = False

        #I -> nothing rate \rho**4 
        rec2 = (tot > 3 )   
        I[rec2] = False
        I[(totI>1) & (tot>2)] = True

        A[...] = False


    def init(self,size):
        X= np.zeros((size,size,self.nbDir),[('E',np.bool),('I',np.bool),('S',np.bool)]) #Excitation, Inhibition, Solvant
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

        self.actNP = np.zeros((size,size),dtype=np.bool_)
        self.activation = ConstantMap('act',size,self.actNP)


        self.mean = 0


        self.init2(size,X)
        #X[Y] = 0
        return X

    def init2(self,size,X):
       #rho = self.getArg('rho')
       rho = self.rho
       S = X['S']
       E = X['E']
       #S[5+2,4,1] = 1
       #E[6+2,5,0] = 1
       #E[5+2,6,3] = 1
       #S[4+2,5,2] = 1
       #X+= (np.random.randint(0,2,(size,size,self.nbDir))).astype(np.bool_)
       #r=size/20
       #X[:,0:size/2-r,:] = (np.random.random((size,size,4)) < 0.7)[:,0:size/2-r,:]
       X['S'] += (np.random.random((size,size,4)) < rho)

    def getViewData(self):
        displayedLayer = self.getArg('displayedLayer')
        if displayedLayer > 4:
                displayedLayer = 0
                self.setArg(displayedLayer=displayedLayer)

        if displayedLayer == 0:
            data = self.getData()
        elif displayedLayer == 1:#sum of every particule
            data = np.sum(self._data['E'],axis=2)+ np.sum(self._data['I'],axis=2)+ np.sum(self._data['S'],axis=2)
        elif displayedLayer == 2:
            data =  np.sum(self._data['S'],axis=2)
        elif displayedLayer == 3:
            data =  np.sum(self._data['E'],axis=2)
        elif displayedLayer == 4:
            data =  np.sum(self._data['I'],axis=2)
        

        return data

    def getData(self):
        iExc = self.getArg('iExc')
        iInh = self.getArg('iInh')
        data = iExc*np.sum(self._data['E'],axis=2) - iInh*np.sum(self._data['I'],axis=2)
        return data

    def _onParamsUpdate(self,dnfSize,iExc,iInh):
        iExc = iExc/(dnfSize**2) * (40**2)/10.
        iInh = iInh/(dnfSize**2) * (40**2)/10.

        return dict(iExc=iExc,iInh=iInh)


    def onClick(self,x,y):
        self.lock.acquire()
        size = self.getArg('size')
        gauss = utils.gauss2d(size,True,1,size/20.,x,y)
        spot = np.where(gauss > 0.5,1,0).astype(np.bool_)
        #spot4 = np.dstack([spot]*4)
        self.actNP |= spot
        self.lock.release()

@profile
def choice(size,p,col,col1,rand,colDir):
    ret = np.zeros((size,size),dtype=np.bool_)
    ret[p] = True #a particule moves if there is no collision
    ret[p&colDir] = False #if there was a colision in our direction, we move!
    ret[(~p) & col & (~colDir)] = True #there was a collision with only our particules
    ret[(~p) & col1 & (~colDir) & rand] = True #there was a collision with only one particule. Rand chose the direction of the propagation
    return ret

def makeBorder(X):
    return cv2.copyMakeBorder(X,1,1,1,1,cv2.BORDER_WRAP).astype(np.bool_)

