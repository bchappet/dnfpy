import numpy as np
import dnfpy.controller.runner as runner
from dnfpyUtils.scenarios.scenarioRobustness import ScenarioRobustness
from dnfpyUtils.scenarios.scenarioSwitch import ScenarioSwitch
from dnfpyUtils.scenarios.scenarioNoise import ScenarioNoise
from dnfpyUtils.scenarios.scenarioSwitchWM import ScenarioSwitchWM
from dnfpyUtils.scenarios.scenarioStatic import ScenarioStatic
from dnfpyUtils.models.modelDNF import ModelDNF
from pso import QtApp
from PyQt4 import QtGui
from psoDNF import PSODNF
class PSODNFWM(PSODNF):
    """Particle swarm optimisation class"""

    def getConstantParamsDict(self):
        return dict(size=49,model='cnft',activation='step')

    def evaluate(self,indiv):
        #TODO have a list of scenario
        scenarioStatic = ScenarioStatic(timeStim=1.2)
        scenarioWM = ScenarioSwitchWM()

        model =  self.getModel(indiv)
        timeEnd = 20
        allowedTime = 10e10

        (error,wellClusterized,self.time,convergence,maxNbAct,meanNbAct,elapsedTime,errorShape,compEmpty)\
                         = runner.launch(model, scenarioStatic, timeEnd,allowedTime)
        if not(convergence):
            conv = 1.
        else:
            conv = convergence/10.

        f1 = (conv+ compEmpty +error)/3.

        if f1 < 0.5:
            (error,wellClusterized,self.time,convergence,maxNbAct,meanNbAct,elapsedTime,errorShape,compEmpty,wrongNumberOfCluster)  \
                         = runner.launch(model, scenarioWM, timeEnd,allowedTime)
            f2 = (wrongNumberOfCluster + compEmpty + error)/3.
        else:
            f2 = 1


        return 0.5*(f1+f2)




if __name__ == "__main__":
    import sys
    app = QtGui.QApplication([""])
    view = QtApp()
    model = PSODNFWM(view,swarmSize=100,nbEvaluationMax=30000,nbThread=8,omega=-0.2144,phiP=-0.4040,phiG=1.03249)
    view.setModel(model)
    model.start()
    sys.exit(app.exec_())
    res = (model.bestX,model.bestFitness)
    print(res)




