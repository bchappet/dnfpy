import numpy as np
import math



from dnfpy.core.map2D import Map2D


class STDPLearningMap(Map2D):
    """
    Adaptive weights map
    _data contains a kernel (sizeKernel*sizeKernel) for every coordinate
    saveSource: (list) to implement STDP we save the last source activation
    last timeLTP matrices


    children:
        source : the presynaptic neurons activation


    """

    def __init__(self,name,size,dt,sizeKernel,timeLTP=0.6,alphaP=0.004,betaP=0,alphaD=0.003,betaD=0,
                 wMin=-0.1,wMax=0.1,**kwargs):
        #threshold = 40000.
        #wMin = wMin / threshold
        #wMax = wMax/threshold
        #alphaD = alphaD/threshold
        #alphaP = alphaP/threshold
        print("alphaP : %s, alphaD: %s"%(alphaP,alphaD))
        print("wMin: %s, wMax: %s"%(wMin,wMax))

        super(STDPLearningMap,self).__init__(name,size,dtype=np.object,dt=dt,sizeKernel=sizeKernel,
                                         timeLTP=timeLTP,
                                         alphaP=alphaP,betaP=betaP,
                                         alphaD=alphaD,betaD=betaD,
                                         wMin=wMin,wMax=wMax,**kwargs)
        self.saveSource = []
        self.indicesActivated = [] #save the coord of the changed weights


    def changeSynapse(self,coord,alphaP,alphaD,indicesLTP):
        self._data[coord[0],coord[1]] -= alphaD
        self._data[coord[0],coord[1]][indicesLTP] += 2*alphaP

    def clipWeights(self,coord,wMin,wMax):
        array = self._data[coord[0],coord[1]]
        #in place clipping
        np.clip(array,wMin,wMax,array)


    def applyNeighbours(self,coord,alphaP,alphaD,indicesLTP,size):
                #version bourrin
                self.changeSynapse(self.wrap(coord+np.int32([0,1]),size),alphaP,alphaD,indicesLTP)
                self.changeSynapse(self.wrap(coord+np.int32([1,0]),size),alphaP,alphaD,indicesLTP)
                self.changeSynapse(coord-np.int32([0,1]),alphaP,alphaD,indicesLTP)
                self.changeSynapse(coord-np.int32([1,0]),alphaP,alphaD,indicesLTP)

    def wrap(self,coord,size):
        return coord % size

    def _compute(self,size,sizeKernel,source,timeLTP,dt,alphaP,betaP,alphaD,betaD,
                 wMin,wMax):

        sumLastSources = sum(self.saveSource)
        indicesLTP =  np.nonzero(sumLastSources) #indice of the LTP effect on weights

        self.indicesActivated = np.transpose(np.nonzero(source)) #index of the activated neurons: only these one will be modified


        for coord in self.indicesActivated:
                #remove alphaD for LTD and add alphaP for LTP
                self.changeSynapse(coord,alphaP,alphaD,indicesLTP)

                #We share synapses with neighbours neurons gaussianly
                #self.applyNeighbours(coord,alphaP/2.,alphaD/2.,indicesLTP,size)

                self.clipWeights(coord,wMin,wMax)





        #Include the source to the last sources
        self.saveSource.insert(0,source)
        #limit the size with timeLTP
        if len(self.saveSource) > (timeLTP / dt) :
            self.saveSource.pop()




    def reset(self):
        super(STDPLearningMap,self).reset()
        sizeKernel = self._init_kwargs['sizeKernel']
        size = self._init_kwargs['size']
        wMin = self._init_kwargs['wMin']
        wMax = self._init_kwargs['wMax']
        (cols,rows) = (size,size)
        #random init
        for i in range(cols):
            for j in range(rows):
                self._data[i,j] = ((np.random.random((sizeKernel,sizeKernel))) - 0.5)*2 * (wMax-wMin)/100.





