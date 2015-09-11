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
from dnfpyUtils.scenarios.scenarioStatic2 import ScenarioStatic2
from dnfpyUtils.models.modelDNF import ModelDNF

class AGDNF(AlgoGen):
    def __init__(self,view,**kwargs):
            #self.wInh = 0.2
            super(AGDNF,self).__init__(view,**kwargs)

    def getEvaluationParamsDict(self):
        return dict(timeEnd=20,allowedtime=10e10)

    def getConstantParamsDict(self):
        return dict(size=49,model='cnft',activation='step')

    def getListParam(self):
        return ["iExc","iInh","wExc","wInh","th","h"]

    def getBounds(self):
        """return (lowerBounds,upperBounds"""
        lowerBounds = np.array([0,0,0,0,0,-1])
        upperBounds = np.array([10,1,1,10,1,1])
        return (lowerBounds,upperBounds)



    

    def indivToParams(self,indiv):
        """return the parameters dictionary which will be given to the model"""
        # listGen = ["iExc","ik = iInh/iExc","wK=wExc/wInh","wInh","th","thK=h/th"
        paramList = [0] * len(indiv)
        paramList[0] = indiv[0]
        paramList[1] = indiv[1]*indiv[0]
        paramList[2] = indiv[2]*indiv[3]
        paramList[3] = indiv[3]
        paramList[4] = indiv[4]
        paramList[5] = indiv[5]*indiv[4]
        return self.indivToDict(paramList)


    def getModel(self,indiv):
        return ModelDNF(**indiv)



    def evaluate(self,indiv):
        #TODO have a list of scenario
        #print(indiv)
        scenarioStatic = ScenarioStatic2(timeStim=1.2)
        scenarioWM = ScenarioSwitchWM()

        model =  self.getModel(indiv)
        timeEnd = 30
        allowedTime = 10

        (error,wellClusterized,time,convergence,maxNbAct,meanNbAct,elapsedTime,errorShape,compEmpty,nbClusterEnd)\
                         = runner.launch(model, scenarioStatic, timeEnd,allowedTime)

        badEnd1 = (nbClusterEnd != 2)*10
        if(error == 0):
            error = 10
        if not(convergence):
            f2  = 10.
            conv = 10.
        else:
            conv = convergence/10.

            model =  self.getModel(indiv)
            (error2,wellClusterized,time,convergence,maxNbAct,meanNbAct,elapsedTime,errorShape,compEmpty,nbClusterEnd,wrongNumberOfCluster)  \
                         = runner.launch(model, scenarioWM, timeEnd,allowedTime)
            badEnd2 = (nbClusterEnd != 2)*10
            if(error == 0):
                error = 10
            if not(convergence):
                f2 =10 +  2*error2+compEmpty+1.5*wrongNumberOfCluster + errorShape +badEnd2

            else:
                #print("F2 : error : %s compEmpty %s"%(error,compEmpty))
                f2 = 2*error2+compEmpty+1.5*wrongNumberOfCluster + errorShape + badEnd2

        f1 = conv+ compEmpty +error + errorShape + badEnd1
        #print("F1 : error : %s compEmpty %s"%(error,compEmpty))


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
    model = AGDNF(view=None,swarmSize=20,nbEvaluationMax=30000,nbThread=6,mutationRate=0.5,nbMutation=1,eliteRatio=0.0,
            bestIndRatio=1.0)
    model.start()

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to exit')
    signal.pause()



