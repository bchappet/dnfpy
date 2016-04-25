import numpy as np
import dnfpy.controller.runner as runner
from dnfpyUtils.scenarios.scenarioRobustness import ScenarioRobustness
from dnfpyUtils.scenarios.scenarioNoise import ScenarioNoise
from dnfpyUtils.scenarios.scenarioSwitch import ScenarioSwitch
from dnfpyUtils.scenarios.scenarioTracking import  ScenarioTracking
from dnfpyUtils.scenarios.scenarioDistracters import ScenarioDistracters
from dnfpyUtils.scenarios.scenarioStatic2 import ScenarioStatic2
from dnfpyUtils.scenarios.scenarioStatic import ScenarioStatic
from dnfpyUtils.models.modelDNF import ModelDNF

from dnfpyUtils.stats.statsMetaModel import StatsMetaModel
from dnfpyUtils.stats.statsTemplate import StatsTemplate
from dnfpyUtils.stats.statsTracking1 import StatsTracking1

from dnfpyUtils.optimisation.spso2006 import Spso
class SpsoDNF(Spso):
    """Particle swarm optimisation class"""

    def __init__(self,evaluationParamsDict = dict(timeEnd=20,allowedTime=10e10),**kwargs):
        self.modelClass = self.getModelClass()
        self.scenarioClass = self.getScenarioClass()
        super().__init__(evaluationFunc=self.evaluate,evaluationParamsDict=evaluationParamsDict,**kwargs)

    def setModelClass(self,modelClass):
        self.modelClass = modelClass

    def getModelClass(self):
        return ModelDNF

    def setScenarioClass(self,scenarioClass):
        self.scenarioClass = scenarioClass

    def getScenarioClass(self):
        return ScenarioTracking

    def getExecutionBounds(self):
        return (1)


    def getListParam(self):
        return ["iExc","iInh","wExc","wInh","h"]

    def getBounds(self,d):
        """return (lowerBounds,upperBounds"""
        z = 10e-6
        lowerBounds = np.array([z,z,z,z,-1])
        upperBounds = np.array([10,1,1,2,1])
        return (lowerBounds,upperBounds)

    def getStartBounds(self,d):
        return self.getBounds(d)



    def getModel(self,indiv):
        return self.modelClass(**indiv)

    def evaluate(self,indiv):
        constPar = self.constantParamsDict
        #scenarioList = [scenarioT,scenarioN,scenarioD]
        scenario = ScenarioStatic(**constPar)
        #scenario = ScenarioNoise(**constPar)
        scenarioList = [scenario,]
        fitnessList = []

        #statistic used
        #statistic = StatsTracking1(**constPar)
        statistic  =StatsTemplate(**constPar)


        #indiv.update(self.constantParamsDict)
        #print("evaluate %s"%indiv)
        model =  self.getModel(indiv)

        timeEnd = self.evaluationParamsDict['timeEnd']
        allowedTime = self.evaluationParamsDict['allowedTime']

        for scenario in scenarioList:
            #statsMetaModel (error,wellClusterized,time,convergence,maxNbAct,meanNbAct,elapsedTime,errorShape,compEmpty,nbClusterEnd)\
            
            res = runner.launch(model, scenario,statistic, timeEnd,allowedTime)
            error = statistic.fitness(res)
            fitnessList.append(error)
            print()
            print("evaluate %s"%indiv)

            print(res,error)
            print()
        return np.mean(np.array(fitnessList))








