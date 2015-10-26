import numpy as np
import dnfpy.controller.runner as runner
from dnfpyUtils.scenarios.scenarioRobustness import ScenarioRobustness
from dnfpyUtils.scenarios.scenarioNoise import ScenarioNoise
from dnfpyUtils.scenarios.scenarioTracking import ScenarioTracking
from dnfpyUtils.scenarios.scenarioDistracters import ScenarioDistracters
from dnfpyUtils.stats.statsTemplate import StatsTemplate
from dnfpyUtils.models.modelDNF import ModelDNF
from pso import PSO
from pso import QtApp
from PyQt4 import QtGui
class PSODNF(PSO):
    """Particle swarm optimisation class"""

    def getExecutionBounds(self):
        return (1)


    def getListParam(self):
        return ["iExc","iInh","wExc","wInh"]

    def getBounds(self):
        """return (lowerBounds,upperBounds"""
        z = 10e-6
        lowerBounds = np.array([z,z,z,z])
        upperBounds = np.array([10,1,1,2])
        return (lowerBounds,upperBounds)

    def getStartBounds(self):
        return self.getBounds()

    def getConstantParamsDict(self):
        return dict(size=49,model='cnft',activation='step')

    def getEvaluationParamsDict(self):
        return dict(timeEnd=20,allowedTime=10e10)


    def indivToParams(self,indiv):
        """return the parameters dictionary which will be given to the model"""
        # listGen = ["iExc","ik = iInh/iExc","wK=wExc/wInh","wInh",
        paramList = [0] * len(indiv)
        paramList[0] = indiv[0]
        paramList[1] = indiv[1]*indiv[0]
        paramList[2] = indiv[2]*indiv[3]
        paramList[3] = indiv[3]
        return self.indivToDict(paramList)



    def getModel(self,indiv):
        return ModelDNF(**indiv)

    def evaluate(self,indiv):
        nbRepet = 10
        scenarioT = ScenarioTracking()
        scenarioN = ScenarioNoise()
        scenarioD = ScenarioDistracters()
        scenarioList = [scenarioT,scenarioN,scenarioD]
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
    model = PSODNF(view,swarmSize=100,nbEvaluationMax=30000,nbThread=8,omega=0.9,phiP=0.9,phiG=0.5)
    view.setModel(model)
    model.start()
    sys.exit(app.exec_())
    res = (model.bestX,model.bestFitness)
    print(res)




