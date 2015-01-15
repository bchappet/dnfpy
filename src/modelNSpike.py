from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.cellular.mapDNFNSpike import MapDNFNSpike
from dnfpy.stats.clusterMap import ClusterMap
from dnfpy.stats.potentialTarget import PotentialTarget
from dnfpy.stats.trackedTarget import TrackedTarget
from dnfpy.stats.errorDist import ErrorDist

class ModelNSpike(Model,Renderable):
    def initMaps(self,size):
        """We initiate the map and link them"""
        #Create maps
        self.aff = InputMap("Inputs",size)
        self.field = MapDNFNSpike("DNF",size)
        self.field.addChildren(aff=self.aff)
        #stats
        self.clusters = ClusterMap("clustMap",sizeNpArr=size,clustSize=0.2)
        self.clusters.addChildren(np_arr=self.field.act)
        self.potentialTarget = PotentialTarget("potentialTarget",sizeInput=size)
        self.potentialTarget.addChildren(input=self.aff)
        self.trackedTarget = TrackedTarget("trackedTargets",sizeArray=size)
        self.trackedTarget.addChildren(
            potentialTarget=self.potentialTarget,clusterMap=self.clusters)
        self.errorDist = ErrorDist("errorDist",sizeArray=size)
        self.errorDist.addChildren(trackedTarget=self.trackedTarget,
                                   clusterMap=self.clusters)

        #return the roots
        return [self.field,self.clusters,self.potentialTarget,self.trackedTarget,
                self.errorDist]
    #override Renderable
    def getArrays(self):
        ret =  [self.aff,self.field]
        ret.extend(self.field.getArrays())
        ret.append(self.clusters)
        #ret.append(self.potentialTarget)
        ret.append(self.trackedTarget)
        ret.append(self.errorDist)
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
