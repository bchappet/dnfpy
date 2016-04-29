from dnfpy.core.map2D import Map2D
import numpy as np
from dnfpyUtils.stats.trajectory import Trajectory

class ErrorShape(Trajectory):
    """
    Input : 
    1) shapeMap : map with the expected shape of the activation
    2) activationMap : map of the activation

    Params:
            model string in ['cnft','spike'] the same as the model given to Model runnable.
            nbAcc if model == spike, the activation will be accumulated during nbAcc

    Output:
    error = sum(|shape - act|/(shape.size**dim))

    Limit cases:
    If shapeMap == 0:
        error =  np.nan 
    If activationMap == 0:
        error =  np.nan

    """
    def __init__(self,*args,model='cnft',nbAcc=4,**kwargs):
        super().__init__(*args,model=model,nbAcc=nbAcc,**kwargs)

        self.listAct = []
        self.listShape = []

    def accum(self,nbAcc,act,shape):
        if len(self.listAct) > nbAcc:
            self.listAct.pop()
            self.listShape.pop()

        self.listAct.insert(0,np.copy(act))
        self.listShape.insert(0,np.copy(shape))
            

            

    def _compute(self,shapeMap,activationMap,model,nbAcc):
        """
        25/04/2016
        """
        assert(shapeMap.shape == activationMap.shape)

        nbOne = np.sum(shapeMap)
        nbZeros = np.sum(shapeMap==0)
        total = shapeMap.size
        if self.getArg('time') >= 1.3:
            if model== 'spike':
                #We accumulate the sctivation and the shape to see the difference inside the shape
                self.accum(nbAcc,activationMap,shapeMap)
                accShape = np.mean(self.listShape,axis=0)/nbAcc
                accAct = np.mean(self.listAct,axis=0)
                if np.sum(accShape) > 0:
                    #Bad activation outside is always bad
                    outsideBadAct = np.sum((shapeMap - activationMap) == -1)/nbZeros*nbAcc
                    insideBadAct = np.sum(1 - accAct[accShape>0])/np.sum(accShape)
                    #print(outsideBadAct,insideBadAct)
                    error = insideBadAct + outsideBadAct
                elif np.sum(activationMap) > 0:
                    error = np.sum(activationMap)/activationMap.size
                else:
                    error = 0.0
            else:
                if nbOne > 0 :
                    outsideBadAct = np.sum((shapeMap - activationMap) == -1)/nbZeros
                    #compute extended activation as sum of several activation
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


if __name__ == "__main__":
    size = 11
    dim = 1
    activation = np.zeros((size))
    shape = np.zeros((size))
    errorShape = ErrorShape("uut",model='spike',activationMap=activation,shapeMap=shape,nbAcc=3)
    errorShape.compute()
    print(errorShape.getData())
    assert(errorShape.getData() == 0.0)

    for i in range(4):
        shape[...] = 0
        shape[4+i:7+i] = 1
        activation[...] = 0
        activation[np.random.randint(4+i,7+i,(1))] = 1
        errorShape.compute()
        print(errorShape.getData())



