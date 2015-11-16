import numpy as np
import dnfpy.controller.runner as runner
from dnfpyUtils.scenarios.scenarioRobustness import ScenarioRobustness
from dnfpyUtils.scenarios.scenarioSwitch import ScenarioSwitch
from dnfpyUtils.scenarios.scenarioNoise import ScenarioNoise
from dnfpyUtils.scenarios.scenarioSwitchWM import ScenarioSwitchWM
from dnfpyUtils.scenarios.scenarioStatic2 import ScenarioStatic2
from dnfpyUtils.models.modelDNF import ModelDNF
from pso import QtApp
from PyQt4 import QtGui
from psoDNF import PSODNF
class PSODNFWM(PSODNF):
    """Particle swarm optimisation class"""

    def getListParam(self):
        #return ["iExc","iInh","wExc","wInh","th","h"]
        return ["iExc","iInh","th","h"]

    def getBounds(self):
        """return (lowerBounds,upperBounds"""
        z = 10e-6
        #lowerBounds = np.array([z,z,z,z,z,-1])
        #upperBounds = np.array([10,1,1,2,1,1])
        lowerBounds = np.array([z,z,z,-1])
        upperBounds = np.array([10,1,1,1])
        return (lowerBounds,upperBounds)



    

    def indivToParams(self,indiv):
        """return the parameters dictionary which will be given to the model"""
        # listGen = ["iExc","ik = iInh/iExc","wK=wExc/wInh","wInh","th","thK=h/th"
        paramList = [0] * len(indiv)
        paramList[0] = indiv[0]
        paramList[1] = indiv[1]*indiv[0]
        #paramList[2] = indiv[2]*indiv[3]
        #paramList[3] = indiv[3]
        paramList[2] = indiv[2]
        paramList[3] = indiv[3]*indiv[2]
        return self.indivToDict(paramList)



    def getConstantParamsDict(self):
        return dict(size=49,model='spike',activation='step',wExc=0.1,wInh=0.2)



    def evaluate(self,indiv):
        scenarioStatic2 = ScenarioStatic2(timeStim=1.2)
        scenarioSwitchWM = ScenarioSwitchWM()

        model =  self.getModel(indiv)
        timeEnd = 20
        allowedTime = 20

        #(error,wellClusterized,time,convergence,maxNbAct,meanNbAct,elapsedTime,errorShape,compEmpty,nbClusterEnd,wrongNumberOfCluster)\
        #                 = runner.launch(model, scenarioSwitchWM, timeEnd,allowedTime)
        (error,wellClusterized,time,convergence,maxNbAct,meanNbAct,elapsedTime,errorShape,compEmpty,nbClusterEnd,wrongNumberOfCluster)\
                         = runner.launch(model, scenarioSwitchWM, timeEnd,allowedTime)

        badEnd1 = np.abs(nbClusterEnd - 2)*10 #malus if bad number of cluster in the end
        badTime = np.abs(timeEnd - time) * 10 #malus if simulation to slow
        if(error == 0):
            error = 10
        if not(convergence):
            f2  = 10.
            conv = 10.
        else:
            conv = convergence/10.

        #print(indiv)
    #    print("time ",time," elapsedTime ",elapsedTime)
     #   print(conv,compEmpty,error,errorShape,badEnd1,nbClusterEnd)
        f1 = conv+ compEmpty +error + errorShape + badEnd1 + badTime + wrongNumberOfCluster
     #   print(f1)
        return f1






if __name__ == "__main__":
    import sys
    app = QtGui.QApplication([""])
    view = QtApp()
    model = PSODNFWM(view,swarmSize=100,nbEvaluationMax=30000,nbThread=8,omega=0.9,phiP=0.9,phiG=0.5)
    view.setModel(model)
    model.start()
    sys.exit(app.exec_())
    res = (model.bestX,model.bestFitness)
    print(res)




