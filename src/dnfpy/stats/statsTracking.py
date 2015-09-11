from dnfpy.stats.clusterMap import ClusterMap
from dnfpy.stats.potentialTarget import PotentialTarget
from dnfpy.stats.trackedTarget import TrackedTarget
from dnfpy.stats.errorDist import ErrorDist
from dnfpy.stats.shapeMap import ShapeMap
from dnfpy.stats.errorShape import ErrorShape
from dnfpy.model.activationMap import ActivationMap
from dnfpy.controller.runnable import Runnable


class StatsTracking(Runnable):
    """
    Stats contains all the statistics maps
    If parameters or map are needed from the model we can fetch them
    in the runner.

    This is the default stats it expect:
        activationMap
        inputMap

    """
    def __init__(self,runner,**kwargs):
        self.mapDict = {}
        self.runner = runner
        self.root = self.initMaps(**kwargs)
        self._addMapsToDict(self.root) #recursively add map to mapDict

    def getRoot(self):
        return self.root

    def getMapDict(self):
        return self.mapDict


    def initMaps(self,clustSize=0.2):

        activationMap = self.runner.getMap("Activation")
        inputMap = self.runner.getMap("Inputs")
        size = inputMap.getArg("size")
        dt = inputMap.getArg("dt")
        wrap = inputMap.getArg("wrap")


        self.clusters = ClusterMap("clusterMap",sizeNpArr=size,dt=dt,clustSize=clustSize)
        self.clusters.addChildren(np_arr=activationMap)
        self.potentialTarget = PotentialTarget("potentialTarget",dt=dt,sizeInput=size)
        self.potentialTarget.addChildren(input=inputMap)
        self.trackedTarget = TrackedTarget("trackedTargets",dt=dt,sizeArray=size)
        self.trackedTarget.addChildren(
            potentialTarget=self.potentialTarget,clusterMap=self.clusters)
        self.errorDist = ErrorDist("errorDist",dt=dt,sizeArray=size)
        self.errorDist.addChildren(trackedTarget=self.trackedTarget,
                                   clusterMap=self.clusters)



        self.shapeMap = ShapeMap("shapeMap",size=size,dt=dt,wrap=wrap,
                                    )
        self.shapeMap.addChildren(
            tracksCenter=self.trackedTarget,inputMap=inputMap)

        #self.activation = ActivationMap("statAct",size,dt,model='cnft',
        #                               th= activationMap.getArg('th'))
        #self.activation.addChildren(field=fieldMap)

        self.errorShape = ErrorShape("errorShape",dt=dt)
        self.errorShape.addChildren(shapeMap=self.shapeMap,activationMap=activationMap)


        return [self.errorDist,self.errorShape]

    def getArrays(self):
        """
        Return a list of stat map to display
        """
        #return [self.clusters,self.potentialTarget,self.trackedTarget,
        #        self.errorDist,self.shapeMap,self.errorShape,self.activation]
        return [self.trackedTarget,self.errorDist]



