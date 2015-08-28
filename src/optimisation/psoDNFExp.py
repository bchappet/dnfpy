from psoDNF import PSODNF
from pso import QtApp
from PyQt4 import QtGui
from dnfpyUtils.models.modelNSpike import ModelNSpike
import numpy as np
from dnfpyUtils.scenarios.scenarioRobustness import ScenarioRobustness
import dnfpy.controller.runner as runner
from dnfpyUtils.scenarios.scenarioSwitch import ScenarioSwitch
from dnfpyUtils.scenarios.scenarioNoise import ScenarioNoise
class PSODNFExp(PSODNF):
    def getListParam(self):
        #correspond to iE,iI,pE,pI
        return ["iExc","iInh","wExc","wInh"]


    def getBounds(self):
        """return (lowerBounds,upperBounds"""
        z = 10e-6
        lowerBounds = np.array([z,z,z,z])
        upperBounds = np.array([10,1,1,1])
        return (lowerBounds,upperBounds)

    def getEvaluationParamsDict(self):
        return dict(timeEnd=20,allowedTime=2)

    def getConstantParamsDict(self):
        return dict(size=49,lateral='doe',activation='step',model='spike')


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

        (errorR,wellClusterizedR,time,convergenceR,maxNbAct,meanNbAct,elapsedTime,errorShapeR,compEmpty)\
                        = runner.launch(model, scenarioR, timeEnd,allowedTime)
        if errorR < 1 and errorShapeR < 3. and convergenceR <30:
#            #print("indiv %s"%indiv)
             #print("error %s shape %s convergence %s"%(errorR,errorShapeR,convergenceR))
            (errorS,wellClusterizedS,time,convergenceS,maxNbAct,meanNbAct,elapsedTime,errorShapeS,compEmpty)\
                            = runner.launch(model, scenarioS, 6.,allowedTime)
            (errorN,wellClusterizedN,time,convergenceN,maxNbAct,meanNbAct,elapsedTime,errorShapeN,compEmpty)\
                           = runner.launch(model, scenarioN, timeEnd,allowedTime)
        else:
            (errorS, wellClusterizedS,errorShapeS,convergenceS) = (10, 10, 10,100)
            (errorN, wellClusterizedN,errorNhapeN,convergenceN) = (10, 10, 10,100)
#
        if convergenceS == None:
            convergenceS = 100
        if convergenceR == None:
            convergenceR = 100
        if convergenceN == None:
            convergenceN = 100
#
        fitnessError = (errorR + errorS + errorN )/3.
        fitnessCluster = (wellClusterizedR + wellClusterizedS + wellClusterizedN)/3.
        fitnessShape = (errorShapeR + errorShapeS + wellClusterizedN)/3.
        fitnessConv = (convergenceR + convergenceS + convergenceN)/3.
        #print("error %s, conv %s, shape %s"%(fitnessError*10,fitnessConv/10.,fitnessShape))

        return fitnessShape + fitnessError*10 + fitnessConv/10.
        #return errorShapeN + errorN*10 + convergenceN/10.



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication([""])
    view = QtApp()
    model = PSODNFExp(view,swarmSize=100,nbEvaluationMax=30000,nbThread=8)
    view.setModel(model)
    model.start()
    sys.exit(app.exec_())
    res = (model.bestX,model.bestFitness)
    print(res)
