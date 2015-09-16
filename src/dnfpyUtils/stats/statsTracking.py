from dnfpyUtils.stats.clusterMap import ClusterMap
from dnfpyUtils.stats.potentialTarget import PotentialTarget
from dnfpyUtils.stats.trackedTarget import TrackedTarget
from dnfpyUtils.stats.errorDist import ErrorDist
from dnfpyUtils.stats.shapeMap import ShapeMap
from dnfpyUtils.stats.errorShape import ErrorShape
from dnfpy.model.activationMap import ActivationMap
from dnfpyUtils.stats.stats import Stats
import time


class StatsTracking(Stats):
    """

    This is the default stats it expect:
        activationMap
        inputMap

    """
    def initMaps(self,clustSize=0.2,expectedNbCluster=1):
        self.processorTime = time.clock()


        activationMap = self.runner.getMap("Activation")
        inputMap = self.runner.getMap("Inputs")
        size = inputMap.getArg("size")
        self.dt = inputMap.getArg("dt")
        wrap = inputMap.getArg("wrap")


        self.clusters = ClusterMap("clusterMap",sizeNpArr=size,dt=self.dt,clustSize=clustSize,expectedNumberOfCluster=expectedNbCluster)
        self.clusters.addChildren(np_arr=activationMap)
        self.potentialTarget = PotentialTarget("potentialTarget",dt=self.dt,sizeInput=size)
        self.potentialTarget.addChildren(input=inputMap)
        self.trackedTarget = TrackedTarget("trackedTargets",dt=self.dt,sizeArray=size)
        self.trackedTarget.addChildren(
            potentialTarget=self.potentialTarget,clusterMap=self.clusters)
        self.errorDist = ErrorDist("errorDist",dt=self.dt,sizeArray=size)
        self.errorDist.addChildren(trackedTarget=self.trackedTarget,
                                   clusterMap=self.clusters)



        self.shapeMap = ShapeMap("shapeMap",size=size,dt=self.dt,wrap=wrap,
                                    )
        self.shapeMap.addChildren(
            tracksCenter=self.trackedTarget,inputMap=inputMap)

        #self.activation = ActivationMap("statAct",size,dt,model='cnft',
        #                               th= activationMap.getArg('th'))
        #self.activation.addChildren(field=fieldMap)

        self.errorShape = ErrorShape("errorShape",dt=self.dt)
        self.errorShape.addChildren(shapeMap=self.shapeMap,activationMap=activationMap)


        return [self.errorDist,self.errorShape]

    def getArrays(self):
        """
        Return a list of stat map to display
        """
        #return [self.clusters,self.potentialTarget,self.trackedTarget,
        #        self.errorDist,self.shapeMap,self.errorShape,self.activation]
        return [self.trackedTarget,self.errorDist]

    def finalize(self):
        """
        Do something when simulation ends
        and return information
        """

        endProcessorTime = time.clock()


        clusterMap = self.clusters
        error = self.errorDist.getArg("mean")
        nbClusterSum = clusterMap.getArg("nbClusterSum")
        simuTime = clusterMap.getArg('time')
        nbIt = simuTime/self.dt

        wellClusterized = nbClusterSum/nbIt
        maxNbAct = clusterMap.getMaxNbAct()
        meanNbAct = clusterMap.getMeanNbAct()
        elapsedTime = endProcessorTime - self.processorTime
        errorShape  = self.errorShape.getArg("mean")
        compEmpty = clusterMap.getArg("nbComputationEmpty")/float(nbIt)
        nbClusterEnd = len(clusterMap.getData())
        if (clusterMap.nbActivation == 0 or clusterMap.getData()[0][0] == -1 ):
                nbClusterEnd = 0
       
        diffNbClustSum = clusterMap.diffNbClusterSum/nbIt
        convergence = self.trackedTarget.getConvergenceTime()
        #print("compEmpty %s, nbCom %s ,it %s"%(compEmpty,model.getMap("clusterMap").getArg("nbComputationEmpty"),float(self.nbIteration)))
        
        #return dict(error=error,wellClusterized=wellClusterized,time=self.time,conv=self.convergence,maxNbAct=maxNbAct,meanNbAct=meanNbAct,elapsedTime=elapsedTime,errorShape=errorShape,compEmpty=compEmpty,nbClusterEnd=nbClusterEnd,diffNbClustSum=diffNbClustSum)
        return (error,wellClusterized,simuTime,convergence,maxNbAct,meanNbAct,elapsedTime,errorShape,compEmpty,nbClusterEnd,diffNbClustSum)





