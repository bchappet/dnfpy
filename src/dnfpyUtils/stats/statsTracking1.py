from dnfpy.model.activationMap import ActivationMap
from dnfpyUtils.stats.stats import Stats
from dnfpyUtils.stats.errorDistSimple import ErrorDistSimple
import time
from dnfpy.core.constantMap import ConstantMap
from dnfpyUtils.stats.targetCenter import TargetCenter
from dnfpyUtils.stats.barycenterMap import BarycenterMap


class StatsTracking1(Stats):
    """

    This is the  stats it expect for one cluster
        activationMap
        inputMap

    """
    def initMaps(self,size,dim,dt=0.1,wrap=True,**kwargs):
        self.processorTime = time.clock()


        activationMap = self.runner.getMap("Activation")
        inputMap = self.runner.getMap("Inputs")

        self.targetList = [0,]
        self.targetListMap = ConstantMap("TargetList",size=size,value=self.targetList)
        self.targetCenter = TargetCenter("Target",dim=dim,inputMap=inputMap,inputSize=size)
        self.targetCenter.addChildren(targetList=self.targetListMap)

        self.barycenter = BarycenterMap("Barycentre",dim=dim,dt=dt)
        self.barycenter.addChildren(map=activationMap)

        self.errorDist = ErrorDistSimple("ErrorDist",dt=dt,sizeMap=size,wrap=True)
        self.errorDist.addChildren(target=self.targetCenter,mesured=self.barycenter)

        self.timeEnd = None




        return [self.errorDist,]

    def getArrays(self):
        """
        Return a list of stat map to display
        """
        #return [self.clusters,self.potentialTarget,self.trackedTarget,
        #        self.errorDist,self.shapeMap,self.errorShape,self.activation]
        return [self.errorDist,self.targetCenter,self.barycenter]

    def fitness(self,result):
        return result[0]

    def finalize(self):
        """
        Do something when simulation ends
        and return information
        """

        #endProcessorTime = time.clock()


        #clusterMap = self.clusters
        #error = self.errorDist.getRMSE()
        self.timeEnd = self.errorDist.getArg('time')
        error = self.errorDist.getMean()
        #simuTime = clusterMap.getArg('time')
        #nbIt = simuTime/self.dt

        #elapsedTime = endProcessorTime - self.processorTime
       
        return (error,)





