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

from dnfpyUtils.scenarios.scenarioSwitchWM import ScenarioSwitchWM
from dnfpyUtils.scenarios.scenarioStatic import ScenarioStatic
from dnfpyUtils.models.modelDNF import ModelDNF

class AGDNF(AlgoGen):
    def __init__(self,view,**kwargs):
            #self.wInh = 0.2
            super(AGDNF,self).__init__(view,**kwargs)

    def getEvaluationParamsDict(self):
        return dict(timeEnd=20,allowedtime=10e10)

    def getListParam(self):
        return ["iExc","iInh","wExc","wInh","h","th"]

    def getBounds(self):
        """return (lowerBounds,upperBounds"""
        lowerBounds = np.array([0,0,0,0,-1,0])
        upperBounds = np.array([10,1,1,10,1,1])
        return (lowerBounds,upperBounds)



    def getConstantParamsDict(self):
        return dict(size=49,model='cnft',activation='step')

    def indivToParams(self,indiv):
        """return the parameters dictionary which will be given to the model"""
        # listGen = ["iExc","ik = iInh/iExc","wK=wExc/wInh","wInh",
        paramList = [0] * len(indiv)
        paramList[0] = indiv[0]
        paramList[1] = indiv[1]*indiv[0]
        paramList[2] = indiv[2]*indiv[3]
        paramList[3] = indiv[3]
        paramList[4] = indiv[4]
        paramList[5] = indiv[5]
        return self.indivToDict(paramList)


    def getModel(self,indiv):
        return ModelDNF(**indiv)



    def evaluate(self,indiv):
        #TODO have a list of scenario
        #print(indiv)
        scenarioStatic = ScenarioStatic(timeStim=1.2)
        scenarioWM = ScenarioSwitchWM()

        model =  self.getModel(indiv)
        timeEnd = 30
        allowedTime = 10e10

        (error,wellClusterized,time,convergence,maxNbAct,meanNbAct,elapsedTime,errorShape,compEmpty)\
                         = runner.launch(model, scenarioStatic, timeEnd,allowedTime)
        if not(convergence):
            conv = 1.
        else:
            conv = convergence/10.

        f1 = conv+ compEmpty +error + errorShape
        #print("F1 : error : %s compEmpty %s"%(error,compEmpty))

        model =  self.getModel(indiv)
        (error2,wellClusterized,time,convergence,maxNbAct,meanNbAct,elapsedTime,errorShape,compEmpty,wrongNumberOfCluster)  \
                         = runner.launch(model, scenarioWM, timeEnd,allowedTime)

        #print("F2 : error : %s compEmpty %s"%(error,compEmpty))
        f2 = 2*error2+compEmpty+1.5*wrongNumberOfCluster + errorShape
        return (f1 + f2)/2. 





def signal_handler(signal, frame):
            print('You pressed Ctrl+C!')
            res = (model.bestX,model.bestFitness)
            print(res)
            print(model.bestXList[:-20])
            sys.exit(0)

if __name__ == "__main__":
    import sys
    global model
    model = AGDNF(view=None,swarmSize=100,nbEvaluationMax=30000,nbThread=8,mutationRate=0.5,nbMutation=1,eliteRatio=0.1)
    model.start()

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to exit')
    signal.pause()








