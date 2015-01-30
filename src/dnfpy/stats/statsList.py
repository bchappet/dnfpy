from dnfpy.stats.clusterMap import ClusterMap
from dnfpy.stats.potentialTarget import PotentialTarget
from dnfpy.stats.trackedTarget import TrackedTarget
from dnfpy.stats.errorDist import ErrorDist


class StatsList(object):
    def __init__(self,size,inputMap,activationMap,dt=0.1):
        self.clusters = ClusterMap("clusterMap",sizeNpArr=size,dt=dt,clustSize=0.2)
        self.clusters.addChildren(np_arr=activationMap)
        self.potentialTarget = PotentialTarget("potentialTarget",dt=dt,sizeInput=size)
        self.potentialTarget.addChildren(input=inputMap)
        self.trackedTarget = TrackedTarget("trackedTargets",dt=dt,sizeArray=size)
        self.trackedTarget.addChildren(
            potentialTarget=self.potentialTarget,clusterMap=self.clusters)
        self.errorDist = ErrorDist("errorDist",dt=dt,sizeArray=size)
        self.errorDist.addChildren(trackedTarget=self.trackedTarget,
                                   clusterMap=self.clusters)

    def getRoots(self):
        return [self.errorDist]

    def getArrays(self):
        """
        Return a list of stat map to display
        """
        return [self.clusters,self.potentialTarget,self.trackedTarget,self.errorDist]

