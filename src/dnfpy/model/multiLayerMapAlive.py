import numpy as np
import cv2
import dnfpy.core.utils as utils
from multiLayerMap import MultiLayerMap

class MultiLayerMapAlive(MultiLayerMap):
    """The only purpose is to warn the view that this map has several layer"""
    def __init_(self,name,size,dt=0.1,nbCol=3,
                 colTh = 0.2,**kwargs):
        nbCol += 1
        super(MultiLayerMapAlive,self).__init__(name,size,dt=dt,nbCol=nbCol,colTh=colTh,
                                           **kwargs)


    def init(self,size):
        self.stackedX = None
        self.currentColor = 1
        nbCol = self._init_kwargs['nbCol']
        self.colors = np.zeros((size,size,nbCol),dtype=np.float)
        return self.initModel(size)

    def initModel(self,size):
        pass


    def sumNeigh(self,X,this=True,neighType='4',**kwargs):
        if neighType == 'conv':
            sumNeigh = cv2.filter2D(X[1:-1,1:-1,:],-1,cv2.flip(kwargs['kernel'],-1),
                                  anchor=(-1,-1),borderType=kwargs['borderType'])
        else:
            if this:
                sumNeigh = X[1:-1,1:-1,:]
            else:
                sumNeigh = 0

            sumNeigh += (   X[:-2,1:-1,:]+
                    X[1:-1,:-2,:]    +    X[1:-1,2:,:]+
                                X[2:  ,1:-1,:])
            if neighType == '8':
                sumNeigh += (X[:-2, : -2]        +X[:-2,2:]
                        +   X[2:,:-2]           +X[2:,2:])
        return sumNeigh



    def updateColors(self,X,this=True,neighType='4',**kwargs):
        nbCol = self.getArg('nbCol')
        colTh = self.getArg('colTh')
        Y = np.where(X >= colTh,X,0)
        self.stackedX = np.dstack([Y]*nbCol)
        pCol = self.colors * self.stackedX
        c = self.colors[1:-1,1:-1]
        sumNeigh = self.sumNeigh(pCol,this,neighType,**kwargs)
        maxNeighs = self.getMaxCoords(sumNeigh)
        #config 1 with uint8: color merges
        #c[...] = 0
        c[maxNeighs] +=1

        #c[maxNeighs] += 0.1



        c[:,:,0] = 0

        self.moveColors()

    def moveColors(self):
        c = self.colors
        for i in range(1,c.shape[2]):
            self.moveColor(c[:,:,i])

    def moveColor(self,X):
        x = X[1:-1,1:-1]
        lx = (                  X[:-2,1:-1]+
              X[1:-1,:-2]    -4*x +   X[1:-1,2:]+
                                X[2:  ,1:-1])
        x += lx/4
        np.clip(x,0,255,out=x)



    def eraseColorThreshold(self,X):
        colTh = self.getArg('colTh')
        coordInf= X < colTh
        self.colors[coordInf] = False #shut down color belox threshold


    def getColors(self):
        return self.colors

    def getType(self):
        return 'discrete'

    def getMaxCoords(self,v):
        """
        return the coordinate of the maximal coord for the third axis
        """
        rang = range(v.shape[0])
        grid = np.meshgrid(rang,rang)
        coords3 = np.argmax(v,axis=2)
        coords = (grid[1],grid[0],coords3)
        return coords

    def printROI(self,name,a,x,y,r):
        ret = name
        if len(a.shape) > 2:
            for i in range(a.shape[2]):
                ret += "\n" + str(i)+" :\n" + str(a[x-r:x+r+1,y-r:y+r+1,i])
        else:
            ret += "\n" + str(a[x-r:x+r+1,y-r:y+r+1])
        return ret



    def colorise(self,arr,value=True):

        #print("currentColor %s"%self.currentColor)
        colTh = self.getArg('colTh')
        coord = arr > colTh
        #print("coord %s"%(coord,))

        for i in range(self.colors.shape[2]):
            ai = self.colors[:,:,i]
            ai[coord] = False
            #print ai

        a2 = self.colors[:,:,self.currentColor]
        a2[coord] = value

    def score(self):
        li = []
        for i in range(self.colors.shape[2]):
            li.append(np.sum(self.colors[:,:,i]))
        return li

    def onRClick(self,x,y):
        self.changeColor()
        print self.score()
        print self.printROI("col",self.colors,y,x,3)

    def changeColor(self):
        nbCol = self.getArg('nbCol')
        self.currentColor = (self.currentColor + 1 ) % (nbCol -1 ) + 1
        print("curentColor : %s"%self.currentColor)
