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
from pso import PSO
from pso import QtApp
from PyQt4 import QtGui
class PSODNF(PSO):
    """Particle swarm optimisation class"""

    def getExecutionBounds(self):
        return (1)


    def getListParam(self):
        return ["iExc","iInh","wExc"]

    def getBounds(self):
        """return (lowerBounds,upperBounds"""
        z = 1e-10
        lowerBounds = np.array([z,z,z,])
        upperBounds = np.array([20,20,1,])
        return (lowerBounds,upperBounds)

    def getStartBounds(self):
        return self.getBounds()

    def getConstantParamsDict(self):
        return dict(size=49,model='cnft',activation='step',dim=2,wInh=1.0,h=0,th=0.64)

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
        #paramList[3] = indiv[3]
        #paramList[4] = indiv[4]*indiv[3]
        #paramList[2] = indiv[2]#*indiv[3]
        #paramList[3] = indiv[3]
        
        return self.indivToDict(paramList)
        #return self.indivToDict(indiv)

    @staticmethod
    def curveCrossesZero(Y):
            """
            Return indices of elements after which a crossing occurs
            """
            return np.where(np.diff(np.sign(Y)))[0]



    def constraints(self,indiv):
            """
            indiv dictinary
            We are applying constrains to the individual given to the model

            return 0 if constraints are satisfied
            """
            #th = 0.75
            h = 0
            alpha = 10
            dim = 1
            size = 49

            kE = indiv['iExc']
            kI = indiv['iInh']
            wE = indiv['wExc']
            wI = indiv['wInh']
            th = indiv['th']
            h = indiv['h']

            if(h >= th) or (kE <= kI):
                return 100000




            kE2 = kE*40**dim/alpha
            kI2 = kI*40**dim/alpha



            a = np.linspace(0,size,1000)

            assert(wE > 0)
            assert(wI > 0)
            solution =  dogSolution(a,kE2,kI2,wE,wI)



            zeroCross  = np.where(np.diff(np.sign(solution-th+h)))[0]#solution - th == 0?
            derivative = np.gradient(solution)
            if np.any(derivative[zeroCross] < 0):
                    #stable point
                    return 0
            else:
                    if(len(zeroCross) == 0):
                        #no fixed point, return the minimal distance from 0 
                        mini =  np.min(np.abs(solution -th + h))
                        return mini
                    else:
                        #fixed point but unstable, return the slope of the derivative?
                        derivative = np.sum(derivative[zeroCross])
                        return derivative



    def getModel(self,indiv):
        return ModelDNF1D(**indiv)

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
                        errorShape = runner.launch(model, stats,scenario, timeEnd,allowedTime)
                        fitness =  errorShape
                        fitnessList.append(fitness)

                fitness =  np.mean(np.array(fitnessList))
        else:
                fitness= 10000 + constraints
        if np.isnan(fitness):
            fitness = 1000000
        return fitness


def gaussSolution(x,k,w):
    return np.sqrt(np.pi)/2 * k * w *erf(x/w)


def dogSolution(x,kE,kI,wE,wI):
    return gaussSolution(x,kE,wE) - gaussSolution(x,kI,wI)




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




