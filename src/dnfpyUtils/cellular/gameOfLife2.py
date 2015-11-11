import numpy as np
from dnfpy.model.multiLayerMap import MultiLayerMap


class GameOfLife2(MultiLayerMap):
    def __init__(self,name,size,dt=0.1,nbCol=4,colTh=0.2,**kwargs):
        super(GameOfLife2,self).__init__(name,size,dt=dt,
                                         nbCol=nbCol,colTh=colTh,**kwargs)

    def _compute(self):
        X = self._data
        # Count neighbours
        N = (X[0:-2,0:-2] + X[0:-2,1:-1] + X[0:-2,2:] +
             X[1:-1,0:-2]                + X[1:-1,2:] +
             X[2:  ,0:-2] + X[2:  ,1:-1] + X[2:  ,2:])

        # Apply rules
        birth = (N==3) & (X[1:-1,1:-1]==0)
        survive = ((N==2) | (N==3)) & (X[1:-1,1:-1]==1)

        self.updateColors(X,this=True,neighType='8')

        X[...] = 0
        X[1:-1,1:-1][birth | survive] = 1
        #print "X : "
        #print X

        self.eraseColorThreshold(X)


    def getType(self):
        return 'binary'


    def initModel(self,size):
        return np.zeros((size,size),dtype=np.uint8)
        #return np.random.randint(0,2,(size,size))


    def onClick(self,x,y):
        pixel = self._data[y,x]
        pixel = (pixel+1)%2
        self._data[y,x] = pixel

        size = self.getArg('size')
        pattern  = np.zeros((size,size),dtype=np.int8)
        pattern[y,x] = 1
        #print ("the pixel :: %s"%pixel)
        self.colorise(pattern,pixel)



