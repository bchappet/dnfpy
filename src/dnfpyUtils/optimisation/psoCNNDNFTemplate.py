import numpy as np
from scipy.special import erf
import dnfpy.controller.runner as runner
from dnfpyUtils.scenarios.scenarioRobustness import ScenarioRobustness
from dnfpyUtils.scenarios.scenarioNoise import ScenarioNoise
from dnfpyUtils.scenarios.scenarioTracking import ScenarioTracking
from dnfpyUtils.scenarios.scenarioDistracters import ScenarioDistracters
from dnfpyUtils.stats.statsTemplate import StatsTemplate
from dnfpyUtils.stats.statsMetaModel import StatsMetaModel
from dnfpyUtils.models.modelDNF import ModelDNF
from dnfpyUtils.models.modelDNF1D import ModelDNF1D
from dnfpyUtils.models.modelCNNDNF import ModelCNNDNF
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
        z = 1e-10
        lowerBounds = np.array([z,z,z,z])
        upperBounds = np.array([300,100,3,3])
        return (lowerBounds,upperBounds)

    def getStartBounds(self):
        return self.getBounds()

    def getConstantParamsDict(self):
        return dict(size=49,model='cnft',activation='id',dim=2,h=0,th=0.64)

    def getEvaluationParamsDict(self):
        return dict(timeEnd=20,allowedTime=10e10)


    def indivToParams(self,indiv):
        """return the parameters dictionary which will be given to the model"""
        # listGen = ["iExc","ik = iInh/iExc","wK=wExc/wInh","wInh",
        paramList = [0] * len(indiv)
        paramList[0] = indiv[0]
        #paramList[1] = indiv[1] *indiv[0]
        paramList[1] = indiv[1]
        paramList[2] = indiv[2]
        paramList[3] = indiv[3]
        #paramList[4] = indiv[4]*indiv[3]
        #paramList[2] = indiv[2]#*indiv[3]
        #paramList[3] = indiv[3]
        
        return self.indivToDict(paramList)
        #return self.indivToDict(indiv)




    def getModel(self,indiv):
        return ModelCNNDNF(**indiv)

    def evaluate(self,indiv):
        nbRepet = 1
        scenarioT = ScenarioTracking()
        scenarioN = ScenarioNoise()
        scenarioD = ScenarioDistracters()
        scenarioR = ScenarioRobustness()
        scenarioList = [scenarioR]
        fitnessList  = []

        #constraints = self.constraints(indiv)
        constraints = 0
        if constraints == 0:

                stats = StatsTemplate()
                #stats = StatsMetaModel()

                #indiv.update(self.constantParamsDict)
                #print("evaluate %s"%indiv)
                model =  self.getModel(indiv)

                timeEnd = self.evaluationParamsDict['timeEnd']
                allowedTime = self.evaluationParamsDict['allowedTime']

                for repet in range(nbRepet):
                    for scenario in scenarioList:
                        #errorShape,errorDist = runner.launch(model, stats,scenario, timeEnd,allowedTime)
                        #fitness = (errorDist*100 + errorShape)/2
                        errorShape,nanRatio,timeEnd = runner.launch(model, stats,scenario, timeEnd,allowedTime)
                        assert(timeEnd>=20.0)
                        fitness =  (errorShape + nanRatio*0.1)
                        if fitness <= 0.0:
                                #print("Problem for indiv",indiv," the fitness was ", fitness," with ",errorShape,",",nanRatio,",",timeEnd)
                                fitness = 1000000
                                
                        fitnessList.append(fitness)

                fitness =  np.mean(np.array(fitnessList))
        else:
                fitness= 10000 + constraints
        if np.isnan(fitness):
            fitness = 1000000
        return fitness




if __name__ == "__main__":
    import sys
    app = QtGui.QApplication([""])
    view = QtApp()
    model = PSODNF(view,swarmSize=100,nbEvaluationMax=30000,nbThread=8,omega=0.9,phiP=1.2,phiG=1.2) 
    #model = PSODNF(view,swarmSize=100,nbEvaluationMax=30000,nbThread=8,omega=0.9,phiP=0.4,phiG=0.4) #not good
    #model = PSODNF(view,swarmSize=100,nbEvaluationMax=30000,nbThread=8,omega=0.721347, phiP=1.193147,phiG=1.193147) #not good
    view.setModel(model)
    model.start()
    sys.exit(app.exec_())
    res = (model.bestX,model.bestFitness)
    print(res)




