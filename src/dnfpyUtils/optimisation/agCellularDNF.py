from ag import AlgoGen
import dnfpy.controller.runner as runner
from dnfpyUtils.scenarios.scenarioRobustness import ScenarioRobustness
from dnfpyUtils.scenarios.scenarioSwitch import ScenarioSwitch
from dnfpyUtils.scenarios.scenarioNoise import ScenarioNoise
from pso import QtApp
from PyQt4 import QtGui
from ag import AlgoGen

from dnfpyUtils.models.modelDNFCellular import ModelDNFCellular
import numpy as np
import signal
import sys


class AGCellularDNF(AlgoGen):
    def __init__(self,view,nbBit=6,**kwargs):
            self.nbBit = nbBit
            super(AGCellularDNF,self).__init__(view,**kwargs)

    def getEvaluationParamsDict(self):
        return dict(timeEnd=20,allowedtime=10e10)

    def getListParam(self):
        return xrange(2**self.nbBit)

    def getBounds(self):
        """return (lowerBounds,upperBounds"""
        lowerBounds = np.zeros((self.nbDim))
        upperBounds = np.ones((self.nbDim))
        return (lowerBounds,upperBounds)

    def getStartBounds(self):
        """return (lowerBounds,upperBounds"""
        return self.getBounds()

    def mutationPoint(self,indiv,position):
        """We invert the bit"""
        return ~indiv[position]

    def initPopulation(self,nb,dim,lower,upper):
        """Init random pop"""
        x = np.zeros((nb,dim),dtype=np.bool_)
        for i in range(nb):
            x[i] = np.random.randint(0,2,(dim))
        return x

    def indivToDict(self,paramList):
        return paramList



    
    def getConstantParamsDict(self):
        return dict(size=49,model='spike')

    def getEvaluationParamsDict(self):
        return dict(timeEnd=20,allowedTime=10e10)


    def getModel(self,indiv):
        #print(indiv.astype(np.uint8))
        return ModelDNFCellular(lut=indiv)

    def evaluate(self,indiv):
        scenarioR = ScenarioRobustness()
        scenarioS = ScenarioSwitch()
        scenarioN = ScenarioNoise()

        model =  self.getModel(indiv)

        timeEnd = self.evaluationParamsDict['timeEnd']
        allowedTime = self.evaluationParamsDict['allowedTime']


        (errorN,wellClusterizedN,time,convergenceN,maxNbAct,meanNbAct,elapsedTime,errorShapeN)\
                         = runner.launch(model, scenarioN, timeEnd,allowedTime)
        
        if convergenceN == None:
            convergenceN = 100
        if errorShapeN == 0:
            errorShapeN = 10
        if errorN == 0:
            errorN=1
#
        print(errorShapeN,errorN*10,convergenceN/10.)
        return errorShapeN + errorN*10 + convergenceN/10.



def signal_handler(signal, frame):
            print('You pressed Ctrl+C!')
            res = (model.bestX,model.bestFitness)
            print(res)
            print(model.bestXList[:-20])
            sys.exit(0)

if __name__ == "__main__":
    import sys
    global model
    model = AGCellularDNF(view=None,swarmSize=100,nbEvaluationMax=30000,nbThread=8,mutationRate=1.,nbMutation=15)
    model.start()

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to exit')
    signal.pause()








