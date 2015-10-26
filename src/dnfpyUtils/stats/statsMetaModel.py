from dnfpyUtils.stats.simpleShapeMap import SimpleShapeMap
from dnfpyUtils.stats.errorShape import ErrorShape
from dnfpy.model.activationMap import ActivationMap
from dnfpyUtils.stats.stats import Stats
from dnfpy.core.constantMap import ConstantMap

from dnfpyUtils.stats.lyapunovMap import LyapunovMap

class StatsMetaModel(Stats):
    """

    This is the stats to compute the meta model it expect:
        activationMap
        inputMap

    """
    def initMaps(self,shapeThreshold=0.4):

        activationMap = self.runner.getMap("Activation")
        inputMap = self.runner.getMap("Inputs")
        convMap = self.runner.getMap("Lateral")
        dnfMap = self.runner.getMap("Potential")

        th = dnfMap.getArg("th")
        h = dnfMap.getArg("h")

        size = inputMap.getArg("size")
        dim = inputMap.getArg("dim")


        self.lyapunov = LyapunovMap("Lyapunov",th=th,h=h)
        self.lyapunov.addChildren(conv=convMap,input=inputMap,act=activationMap)


        return [self.lyapunov,]


    def applyContext(self):
        #We make sure that the target 0 is focused on
        self.track0 = self.runner.getMap("Inputs_track0")
        self.track1 = self.runner.getMap("Inputs_track1")
        self.track0.setParams(intensity=1.)
        self.track1.setParams(intensity=0.95)

    def getArrays(self):
        return [self.lyapunov,]



    def finalize(self):
        return []

