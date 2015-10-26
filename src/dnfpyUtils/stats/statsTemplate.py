from dnfpyUtils.stats.simpleShapeMap import SimpleShapeMap
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
    def initMaps(self,shapeThreshold=0.4):

        activationMap = self.runner.getMap("Activation")
        inputMap = self.runner.getMap("Inputs")
        size = inputMap.getArg("size")

        self.targetList = [0,]
        self.targetListMap = ConstantMap("TargetList",size=size,value=self.targetList)
        self.simpleShape = SimpleShapeMap("SimpleShape",size=size,dt=self.dt,inputMap=inputMap,shapeThreshold=shapeThreshold)
        self.simpleShape.addChildren(targetList=self.targetListMap)
        self.errorShape = ErrorShape("errorShape",dt=self.dt)
        self.errorShape.addChildren(shapeMap=self.simpleShape,activationMap=activationMap)

        return [self.errorShape,]


    def applyContext(self):
        #We make sure that the target 0 is focused on
        self.track0 = self.runner.getMap("Inputs_track0")
        self.track1 = self.runner.getMap("Inputs_track1")
        self.track0.setParams(intensity=1.)
        self.track1.setParams(intensity=0.95)

    def getArrays(self):
        return [self.simpleShape,self.errorShape]



    def finalize(self):
        return [self.errorShape.getArg("mean"),]

