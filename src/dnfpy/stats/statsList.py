from dnfpy.stats.clusterMap import ClusterMap
from dnfpy.stats.potentialTarget import PotentialTarget
from dnfpy.stats.trackedTarget import TrackedTarget
from dnfpy.stats.errorDist import ErrorDist
from dnfpy.stats.shapeMap import ShapeMap
from dnfpy.stats.errorShape import ErrorShape
from dnfpy.model.activationMap import ActivationMap


class StatsList(object):
    """
    latMap is a map where we can getParams: iExc_,iInh_ wExc_ or pExc_
    """
    def __init__(self,size,inputMap,activationMap,fieldMap,
                 dt=0.1,shapeType='gauss',wrap=True,th=0.75):
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



        self.shapeMap = ShapeMap("shapeMap",size=size,dt=dt,wrap=wrap,
                                 shapeType=shapeType,
                                    )
        self.shapeMap.addChildren(
            tracksCenter=self.trackedTarget,inputMap=inputMap)

        #self.activation = ActivationMap("statAct",size,dt,model='cnft',
        #                               th= activationMap.getArg('th'))
        #self.activation.addChildren(field=fieldMap)

        self.errorShape = ErrorShape("errorShape",dt=dt)
        self.errorShape.addChildren(shapeMap=self.shapeMap,activationMap=activationMap)



    def getRoots(self):
        return [self.errorDist,self.errorShape]

    def getArrays(self):
        """
        Return a list of stat map to display
        """
        #return [self.clusters,self.potentialTarget,self.trackedTarget,
        #        self.errorDist,self.shapeMap,self.errorShape,self.activation]
        return [self.trackedTarget,self.errorDist]

