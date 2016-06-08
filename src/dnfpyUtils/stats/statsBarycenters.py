from dnfpyUtils.stats.clusterMapList import ClusterMapList
from dnfpyUtils.stats.potentialTarget import PotentialTarget
from dnfpyUtils.stats.trackedTarget import TrackedTarget
from dnfpyUtils.stats.errorDist import ErrorDist
from dnfpyUtils.stats.shapeMap import ShapeMap
from dnfpyUtils.stats.errorShape import ErrorShape
from dnfpy.model.activationMap import ActivationMap
from dnfpyUtils.stats.stats import Stats
from dnfpyUtils.stats.goodFocus import GoodFocus
import time


class StatsBarycenters(Stats):
    """

    it expect:
        activationMap

    """
    def initMaps(self,size,dim,clustSize=0.2,min_samples=4,
            dt=0.1,wrap=True,mapUnderStats="",**kwargs):
        self.processorTime = time.clock()


        activationMap = self.runner.getMap("Activation"+mapUnderStats)

        self.clusters = ClusterMapList("Clusters",dim=dim,dt=dt,sizeMap=size,
                min_samples=min_samples,clustSize=clustSize)
        self.goodFocus = GoodFocus("GoodFocus",dt=dt)
                
        self.clusters.addChildren(map=activationMap)
        self.goodFocus.addChildren(clusterList=self.clusters)


        return [self.goodFocus]

    def getArrays(self):
        """
        Return a list of stat map to display
        """
        #return [self.clusters,self.potentialTarget,self.trackedTarget,
        #        self.errorDist,self.shapeMap,self.errorShape,self.activation]
        return [self.clusters,self.goodFocus]

    def finalize(self):
        """
        Do something when simulation ends
        and return information
        """
        super().finalize()




        return []





