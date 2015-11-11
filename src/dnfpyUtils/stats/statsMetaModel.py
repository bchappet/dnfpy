from dnfpyUtils.stats.simpleShapeMap import SimpleShapeMap
from dnfpyUtils.stats.errorShape import ErrorShape
from dnfpy.model.activationMap import ActivationMap
from dnfpyUtils.stats.stats import Stats
from dnfpy.core.constantMap import ConstantMap

from dnfpyUtils.stats.lyapunovMap import LyapunovMap
from dnfpyUtils.stats.metaModelMap import MetaModelMap
from dnfpyUtils.stats.metaBubbleMap import MetaBubbleMap
from dnfpyUtils.stats.barycenterMap import BarycenterMap 

from dnfpyUtils.stats.movingAverage import MovingAverage
from dnfpyUtils.stats.derivative import Derivative
from dnfpyUtils.stats.errorDistSimple import ErrorDistSimple
class StatsMetaModel(Stats):
    """

    This is the stats to compute the meta model it expect:
        activationMap
        inputMap

    """
    def initMaps(self,shapeThreshold=0.4):

        activationMap = self.runner.getMap("Activation")
        inputMap = self.runner.getMap("Inputs")
        self.track0 = self.runner.getMap("Inputs_track0")
        convMap = self.runner.getMap("Lateral")
        dnfMap = self.runner.getMap("Potential")


        th = dnfMap.getArg("th")
        h = dnfMap.getArg("h")
        dt = dnfMap.getArg("dt")
        wrap = dnfMap.getArg("wrap")

        size = inputMap.getArg("size")
        dim = inputMap.getArg("dim")


        #self.lyapunov = LyapunovMap("Lyapunov",fieldMap=dnfMap)
        #self.lyapunov.addChildren(conv=convMap,input=inputMap,act=activationMap)
        #self.lyapunovMA = MovingAverage("LyapunovMA",dt=dt,windowSize=1.)
        #self.lyapunovMA.addChildren(data=self.lyapunov)
        #self.lyapunovDerivative = Derivative("LyapunovDerivative",dt=dt)
        #self.lyapunovDerivative.addChildren(data=self.lyapunovMA)

        self.metaModel = MetaModelMap("Meta-Model",self.track0,dt=dt,dim=1,a=0.3,tau=0.64)


        self.metaBubble = MetaBubbleMap("Meta-Bubble",size=size,dim=dim,dt=dt,activationMap=activationMap,wrap=wrap,width=0.1)
        self.metaBubble.addChildren(metaModel=self.metaModel)


        self.errorShape = ErrorShape("ErrorShape",dt=dt)
        self.errorShape.addChildren(shapeMap=self.metaBubble,activationMap=activationMap)

        self.barycenter = BarycenterMap("Barycentre",dim=dim,dt=dt)
        self.barycenter.addChildren(map=activationMap)

        self.errorDist = ErrorDistSimple("ErrorDist",dt=dt,sizeMap=size,wrap=True)
        self.errorDist.addChildren(target=self.metaModel,mesured=self.barycenter)







        return [self.errorShape,self.errorDist]


    def applyContext(self):
        #We make sure that the target 0 is focused on
        self.track0.setParams(intensity=1.)
        #init meta model to the track
        self.track0.compute()
        z = self.track0.getCenter()/self.track0.getArg("size")
        self.metaModel.initPos(z)
        try:
            self.track1 = self.runner.getMap("Inputs_track1")
            self.track1.setParams(intensity=0.95)
        except:
                pass #TODO adapt to n tracks

    def getArrays(self):
        return [self.metaModel,self.metaBubble,self.errorShape,self.barycenter,self.errorDist]



    def finalize(self):
        return [self.errorShape.getMean(),self.errorDist.getMean()]

