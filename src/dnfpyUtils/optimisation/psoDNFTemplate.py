import numpy as np

from scipy.special import erf
import dnfpy.controller.runner as runner
from dnfpyUtils.scenarios.scenarioRobustness import ScenarioRobustness
from dnfpyUtils.scenarios.scenarioNoise import ScenarioNoise
from dnfpyUtils.scenarios.scenarioTracking import ScenarioTracking
from dnfpyUtils.scenarios.scenarioDistracters import ScenarioDistracters
from dnfpyUtils.scenarios.competition import Competition
from dnfpyUtils.scenarios.workingMemory import WorkingMemory
from dnfpyUtils.scenarios.workingMemoryShift import WorkingMemoryShift
from dnfpyUtils.stats.statsTemplate import StatsTemplate
from dnfpyUtils.stats.statsMetaModel import StatsMetaModel
from dnfpyUtils.models.modelDNF import ModelDNF
from dnfpyUtils.models.modelDNF1D import ModelDNF1D
from dnfpyUtils.optimisation.psoDNF import PSODNF
class PsoDNFTemplate(PSODNF):
    """Particle swarm optimisation class"""

    def getExecutionBounds(self):
        return (1)


    def getListParam(self):
        return ["iExc","iInh","wExc","wInh","h","th","tau"]#,"beta"]

    def getBounds(self):
        """return (lowerBounds,upperBounds"""
        z = 1e-10
        lowerBounds = np.array([z,z,0.01,0.01,-1,0,0]) #if w = 0.00000000001 , we have only one pixel at 1 in the lateral weights
        upperBounds = np.array([1000,1,1,1,1,1,10])
        return (lowerBounds,upperBounds)

    def getStartBounds(self):
        return self.getBounds()

    def getConstantParamsDict(self):
        return dict(size=49,model='cnft',activation='step',dim=1)

    def getEvaluationParamsDict(self):
        return dict(timeEnd=40,allowedTime=10e10)


    def indivToParams(self,indiv):
        """return the parameters dictionary which will be given to the model"""
        # listGen = ["iExc","ik = iInh/iExc","wK=wExc/wInh","wInh",
        paramList = [0] * len(indiv)
        paramList[0] = indiv[0]
        paramList[1] = indiv[1] *indiv[0]
        paramList[2] = indiv[2] *indiv[3]
        paramList[3] = indiv[3]
        paramList[4] = indiv[4]
        paramList[5] = indiv[5]
        paramList[6] = indiv[6]
        #paramList[3] = indiv[3]
        #paramList[4] = indiv[4]*indiv[3]
        #paramList[2] = indiv[2]#*indiv[3]
        #paramList[3] = indiv[3]
        
        return self.indivToDict(paramList)
        #return self.indivToDict(indiv)

    def getScenarioClass(self):
        return WorkingMemory

    def getModelClass(self):
        return ModelDNF1D


    def evaluate(self,indiv):
        nbRepet = 1
        scenarioList = [self.scenarioClass(**self.constantParamsDict)]
        stats = StatsTemplate(**self.constantParamsDict)
        #stats = StatsMetaModel()

        fitnessList  = []

        #print("evaluate %s"%indiv)
        model =  self.getModel(indiv)

        timeEnd = self.evaluationParamsDict['timeEnd']
        allowedTime = self.evaluationParamsDict['allowedTime']

        for repet in range(nbRepet):
            for scenario in scenarioList:
                #errorShape,errorDist = runner.launch(model, stats,scenario, timeEnd,allowedTime)
                #fitness = (errorDist*100 + errorShape)/2
                errorShape,nbNan,timeEnd = runner.launch(model, stats,scenario, timeEnd,allowedTime)
                fitness =  errorShape
                fitnessList.append(fitness)

        fitness =  np.mean(np.array(fitnessList))
        return fitness

if __name__ == "__main__":
    import sys
    model = PsoDNFTemplate(swarmSize=100,nbEvaluationMax=30000,nbThread=8,omega=0.9,phiP=1.2,phiG=1.2,verbose=True) 
    #model = PSODNF(view,swarmSize=100,nbEvaluationMax=30000,nbThread=8,omega=0.9,phiP=0.4,phiG=0.4) #not good
    #model = PSODNF(view,swarmSize=100,nbEvaluationMax=30000,nbThread=8,omega=0.721347, phiP=1.193147,phiG=1.193147) #not good
    model.run()




