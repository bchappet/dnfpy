from dnfpyUtils.stats.simpleShapeMap import SimpleShapeMap
import numpy as np
from dnfpyUtils.stats.errorShape import ErrorShape
from dnfpy.model.activationMap import ActivationMap
from dnfpyUtils.stats.stats import Stats
from dnfpy.core.constantMap import ConstantMap


class StatsTemplate(Stats):
    """

    This is the default stats it expect:
        activationMap
        inputMap

    """
    def initMaps(self,size=49,dim=1,dt=0.1,shapeThreshold=0.6,**kwargs):


        self.targetList = [0,]
        self.targetListMap = ConstantMap("TargetList",size=size,value=self.targetList)
        self.simpleShape = SimpleShapeMap("SimpleShape",size=size,dim=dim,dt=dt,shapeThreshold=shapeThreshold)
        self.simpleShape.addChildren(targetList=self.targetListMap)
        self.errorShape = ErrorShape("errorShape",dt=dt)
        self.errorShape.addChildren(shapeMap=self.simpleShape)

        return [self.errorShape,]


    def applyContext(self):
        #We make sure that the target 0 is focused on
        inputMap = self.runner.getMap("Inputs")
        self.simpleShape.addChildren(inputMap=inputMap)

        activationMap = self.runner.getMap("Activation")
        self.errorShape.addChildren(shapeMap=self.simpleShape,activationMap=activationMap)

    def getArrays(self):
        return [self.simpleShape,self.errorShape]


    def fitness(self,result):
        [rmse,nanRatio,timeEnd] = result
        return rmse


    def finalize(self):
        timeEnd = self.errorShape.getArg('time')
        lenTrace = len(self.errorShape.trace)
        nbNan = np.sum(np.isnan(self.errorShape.getTrace()))
        nanRatio = 1-(lenTrace - nbNan)/lenTrace
        return [self.errorShape.getRMSE(),nanRatio,timeEnd]

