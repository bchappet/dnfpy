from dnfpy.model.activationMap import ActivationMap
import numpy as np
from dnfpyUtils.stats.stats import Stats
from dnfpyUtils.stats.errorDistSimpleList import ErrorDistSimpleList
import time
from dnfpy.core.constantMap import ConstantMap
from dnfpyUtils.stats.targetCenterList import TargetCenterList
from dnfpyUtils.stats.barycenterMapList import BarycenterMapList


class StatsTracking2(Stats):
    """

    This is the  stats it expect for several clusters
        activationMap
        inputMap

    """
    def initMaps(self,size,dim,dt=0.1,wrap=True,**kwargs):
        self.processorTime = time.clock()


        activationMap = self.runner.getMap("Activation")
        inputMap = self.runner.getMap("Inputs")

        self.targetList = [0,]
        self.targetListMap = ConstantMap("TargetList",size=size,value=self.targetList)
        self.targetCenter = TargetCenterList("Target",dim=dim,inputMap=inputMap,inputSize=size)
        self.targetCenter.addChildren(targetList=self.targetListMap)

        self.barycenter = BarycenterMapList("Barycentre",dim=dim,dt=dt)
        self.barycenter.addChildren(map=activationMap,targetCenterList=self.targetCenter)

        self.errorDist = ErrorDistSimpleList("ErrorDist",dt=dt,sizeMap=size,wrap=True)
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

        endProcessorTime = time.clock()


        #clusterMap = self.clusters
        #error = self.errorDist.getRMSE()
        error = self.errorDist.getMean()
        self.timeEnd = self.errorDist.getArg('time')
        #nbIt = simuTime/self.dt

        self.elapsedTime = endProcessorTime - self.processorTime
        meanOutsideAct = np.mean(self.barycenter.outsideAct)
       
        return (error,self.timeEnd,meanOutsideAct,self.elapsedTime)




