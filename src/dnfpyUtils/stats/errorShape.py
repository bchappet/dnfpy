from dnfpy.core.map2D import Map2D
import numpy as np
from dnfpyUtils.stats.trajectory import Trajectory

class ErrorShape(Trajectory):
    """
    Input : 
    1) shapeMap : map with the expected shape of the activation
    2) activationMap : map of the activation

    Output:
    error = sum(|shape - act|/(shape.size**dim))

    Limit cases:
    If shapeMap == 0:
        error =  np.nan 
    If activationMap == 0:
        error =  np.nan

    """
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.listAct = []

    def accum(self,act):
        if len(self.listAct) > 5:
            self.listAct.pop()

        self.listAct.insert(0,act)
            

            

    def _compute(self,shapeMap,activationMap):
        """
        25/04/2016
        """
        self.accum(activationMap)
        assert(shapeMap.shape == activationMap.shape)

        if self.getArg('time') > 2:
            nbOne = np.sum(shapeMap)
            if nbOne > 0 :
                nbZeros = np.sum(shapeMap==0)
                total = shapeMap.size
                outsideBadAct = np.sum((shapeMap - activationMap) == -1)/nbZeros
                #compute extended activation as sum of several activation
                activationMap = np.sum(self.listAct,axis=0)
                insideBadAct = np.sum(1 - activationMap[shapeMap>0])/nbOne
                #insideBadAct = np.sum(activationMap[shapeMap>0]) > 0 #for spike we want at least one activation inside
                error = insideBadAct*0.5 + 0.5 * outsideBadAct
                #error = nbZeros/total*outsideBadAct + nbOne/total*insideBadAct #work well for stantard scenario
                #error = outsideBadAct + insideBadAct #work well for WM
            elif np.sum(activationMap) > 0:
                error = np.sum(activationMap)/activationMap.size
            else:
                error = 0
            self._data = error
            self.trace.append(error)
                

        


    def _compute3(self,shapeMap,activationMap):
        """
        15/11/15
        RMSE : np.sqrt(np.sum((y^ - y)^2/n)
        """
        n = shapeMap.size
        sum = np.sum((shapeMap - activationMap)**2)
        error = sum/n
        self._data = error
        self.trace.append(error)




    def _compute2(self,shapeMap,activationMap,dim):
        if np.all(shapeMap == 0):
            error = np.nan
        elif np.all(activationMap == 0):
            error = np.nan
        else:
            #error = np.sum(np.power(shapeMap*10 - activationMap,2)/(shapeMap.shape[0]*shapeMap.shape[1]*np.sum(shapeMap)))*100
            #error = np.sum(shapeMap == activationMap)/np.sum(shapeMap)
            outsideAct = np.sum((shapeMap - activationMap) == -1)
            badAct = (np.sum(shapeMap == 1) - np.sum(activationMap[shapeMap == 1]))
            error = (badAct+outsideAct) / np.sum(shapeMap) * dim

        self._data = error
        self.trace.append(error)

