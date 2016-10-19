import numpy as np
from getClassUtils import getClassFromName
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

    def __init__(self,scenarioName,statsName,modelName,evaluationParamsDict = dict(timeEnd=20,allowedTime=10e10),scenarioParamsDict={},**kwargs):
        super().__init__(evaluationFunc=self.evaluate,evaluationParamsDict=evaluationParamsDict,**kwargs)
        if isinstance(scenarioName,list):
            assert(len(scenarioName) == len(scenarioParamsDict))
        else:
            scenarioName = [scenarioName,]
            scenarioParamsDict = [scenarioParamsDict,]
        self.scenarioClass = [getClassFromName(sn, 'scenarios') for sn in scenarioName]
        self.statsClass = getClassFromName(statsName,'stats')
        self.modelClass = getClassFromName(modelName, "models")
        self.scenarioParamsDict = scenarioParamsDict


    def getExecutionBounds(self):
        return (1)



    def evaluate(self,indiv):
        constPar = self.constantParamsDict
        scenarioList = []
        for i in range(len(self.scenarioClass)):
            dic = dict(self.scenarioParamsDict[i])
            dic.update(indiv)
            scenarioList.append(self.scenarioClass[i](**dic))

        fitnessList = []
        statistic  =self.statsClass(**indiv)
        model =  self.modelClass(**indiv)
        timeEnd = self.evaluationParamsDict['timeEnd']
        allowedTime = self.evaluationParamsDict['allowedTime']
        for scenario in scenarioList:
            res = runner.launch(model, scenario,statistic, timeEnd,allowedTime)
            error = statistic.fitness(res)
            simuTime = statistic.timeEnd
            if simuTime < timeEnd:
                error = 9999
            #print("simuTime",simuTime)
            #print("error",error)
            fitnessList.append(error)
        return np.mean(np.array(fitnessList))
