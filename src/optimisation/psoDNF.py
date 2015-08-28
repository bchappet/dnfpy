import numpy as np
import dnfpy.controller.runner as runner
from dnfpyUtils.scenarios.scenarioRobustness import ScenarioRobustness
from dnfpyUtils.scenarios.scenarioSwitch import ScenarioSwitch
from dnfpyUtils.scenarios.scenarioNoise import ScenarioNoise
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
        return dict(size=49,model='spike',activation='step')

    def getEvaluationParamsDict(self):
        return dict(timeEnd=20,allowedtime=10e10)


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
        #TODO have a list of scenario
        scenarioR = ScenarioRobustness()
        scenarioS = ScenarioSwitch()
        scenarioN = ScenarioNoise()

        #indiv.update(self.constantParamsDict)
        #print("evaluate %s"%indiv)
        model =  self.getModel(indiv)

        timeEnd = self.evaluationParamsDict['timeEnd']
        allowedTime = self.evaluationParamsDict['allowedTime']

        #(errorR,wellClusterizedR,time,convergenceR,maxNbAct,meanNbAct,elapsedTime,errorShapeR)\
                        #= runner.launch(model, scenarioR, timeEnd,allowedTime)
        (errorN,wellClusterizedN,time,convergenceN,maxNbAct,meanNbAct,elapsedTime,errorShapeN)\
                         = runner.launch(model, scenarioN, timeEnd,allowedTime)
#        if errorR < 1 and errorShapeR < 3. and convergenceR <30:
#            #print("indiv %s"%indiv)
#            #print("error %s shape %s convergence %s"%(errorR,errorShapeR,convergenceR))
#            (errorS,wellClusterizedS,time,convergenceS,maxNbAct,meanNbAct,elapsedTime,errorShapeS)\
                #            = runner.launch(
#                model, scenarioS, 6.,allowedTime)
#            (errorN,wellClusterizedN,time,convergenceN,maxNbAct,meanNbAct,elapsedTime,errorShapeN)\
                #            = runner.launch(model, scenarioN, timeEnd,allowedTime)
#        else:
#            (errorS, wellClusterizedS,errorShapeS,convergenceS) = (10, 10, 10,100)
#            (errorN, wellClusterizedN,errorNhapeN,convergenceN) = (10, 10, 10,100)
#
#        if convergenceS == None:
#            convergenceS = 100
#        if convergenceR == None:
#            convergenceR = 100
        if convergenceN == None:
            convergenceN = 100
#
#        fitnessError = (errorR + errorS + errorN )/3.
#        fitnessCluster = (wellClusterizedR + wellClusterizedS + wellClusterizedN)/3.
#        fitnessShape = (errorShapeR + errorShapeS + wellClusterizedN)/3.
#        fitnessConv = (convergenceR + convergenceS + convergenceN)/3.
        #print("error %s, conv %s, shape %s"%(fitnessError*10,fitnessConv/10.,fitnessShape))

        #return fitnessShape + fitnessError*10 + fitnessConv/10.
        return errorShapeN + errorN*10 + convergenceN/10.




if __name__ == "__main__":
    import sys
    app = QtGui.QApplication([""])
    view = QtApp()
    model = PSODNF(view,swarmSize=100,nbEvaluationMax=30000,nbThread=8)
    view.setModel(model)
    model.start()
    sys.exit(app.exec_())
    res = (model.bestX,model.bestFitness)
    print(res)




