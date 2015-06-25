from psoNSpike import PSONSpike
from pso import QtApp
from PyQt4 import QtGui
from dnfpyUtils.models.modelBsRsdnf import ModelBsRsdnf
import numpy as np
class PSOCASAS(PSONSpike):
    def getBounds(self):
        """return (lowerBounds,upperBounds"""
        z = 10e-6
        lowerBounds = np.array([z,z,z,z])
        upperBounds = np.array([2,1,1,1])
        return (lowerBounds,upperBounds)

    def getStartBounds(self):
        z = 10e-6
        lowerBounds = np.array([z,z,z,z])
        upperBounds = np.array([2,1,1,1])
        return (lowerBounds,upperBounds)

    def getEvaluationParamsDict(self):
        return dict(timeEnd=20,allowedTime=10)


    def getConstantParamsDict(self):
        return dict(size=49,mapType="fast",sizeStream=100)

    def getModel(self,indiv):
        return ModelBsRsdnf(**indiv)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication([""])
    view = QtApp()
    model = PSOCASAS(view,swarmSize=100,nbEvaluationMax=30000,nbThread=8)
    view.setModel(model)
    model.start()
    sys.exit(app.exec_())
    res = (model.bestX,model.bestFitness)
    print(res)
