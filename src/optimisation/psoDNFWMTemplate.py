import numpy as np
import dnfpy.controller.runner as runner
from dnfpyUtils.scenarios.scenarioRobustness import ScenarioRobustness
from dnfpyUtils.scenarios.scenarioNoise import ScenarioNoise
from dnfpyUtils.scenarios.scenarioSwitchWM import ScenarioSwitchWM
from dnfpyUtils.scenarios.scenarioStatic2 import ScenarioStatic2
from dnfpyUtils.models.modelDNF import ModelDNF
from pso import QtApp
from PyQt4 import QtGui
from psoDNFTemplate import PSODNF
from dnfpyUtils.stats.statsTemplate import StatsTemplate
class PSODNFWM(PSODNF):
    """Particle swarm optimisation class"""

    def getListParam(self):
        return ["iExc","iInh","wExc","wInh","th","h"]
        return ["iExc","iInh","h"]

    def getBounds(self):
        """return (lowerBounds,upperBounds"""
        z = 10e-6
        lowerBounds = np.array([z,z,z,z,z,-1])
        upperBounds = np.array([10,1,1,2,1,1])

        #lowerBounds = np.array([z,z,z,-1])
        #upperBounds = np.array([10,1,1,1])

        #lowerBounds = np.array([-10,-10,-10])
        #upperBounds = np.array([10,10,z])
        return (lowerBounds,upperBounds)



    

    def indivToParams(self,indiv):
        """return the parameters dictionary which will be given to the model"""
        # listGen = ["iExc","ik = iInh/iExc","wK=wExc/wInh","wInh","th","thK=h/th"
        paramList = [0] * len(indiv)
        paramList[0] = indiv[0]
        paramList[1] = indiv[1]*indiv[0]
        paramList[2] = indiv[2]*indiv[3]
        paramList[3] = indiv[3]
        paramList[2] = indiv[2]
        paramList[3] = indiv[3]*indiv[2]
        #paramList = indiv
        return self.indivToDict(paramList)



    def getConstantParamsDict(self):
        return dict(size=29,model='cnft',activation='step',wExc=0.1,wInh=0.2)

    def getEvaluationParamsDict(self):
        return dict(timeEnd=30,allowedTime=10e10)

    def evaluate(self,indiv):
        nbRepet = 1
        scenarioList = [
                        #ScenarioStatic2(timeStim=1.2),
                        ScenarioSwitchWM()]
        fitnessList  = []

        stats = StatsTemplate()

        #indiv.update(self.constantParamsDict)
        #print("evaluate %s"%indiv)
        model =  self.getModel(indiv)

        timeEnd = self.evaluationParamsDict['timeEnd']
        allowedTime = self.evaluationParamsDict['allowedTime']

        for repet in range(nbRepet):
            for scenario in scenarioList:
                             fitnessList.append(runner.launch(model, stats,scenario, timeEnd,allowedTime))

        return np.mean(np.array(fitnessList))



   



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication([""])
    view = QtApp()
    model = PSODNFWM(view,swarmSize=100,nbEvaluationMax=30000,nbThread=8,omega=0.9,phiP=0.9,phiG=0.45)
    #model = PSODNFWM(view,swarmSize=200,nbEvaluationMax=100000,nbThread=8,omega=0.721347,phiP=1.193147,phiG=1.193147)
    view.setModel(model)
    model.start()
    sys.exit(app.exec_())
    res = (model.bestX,model.bestFitness)
    print(res)




