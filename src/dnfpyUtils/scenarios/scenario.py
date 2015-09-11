import time
from dnfpy.controller.runnable import Runnable
from dnfpy.stats.statsTracking import StatsTracking
from dnfpy.core.mapND import MapND
class Scenario(Runnable,MapND):
    """
    Mother class for every scenario
    TODO it is a bit to specific for dnf2D with tracking tasks
    The scenario initilize the statistics, change the execution context before starting(in apply context) or during the execution in _apply

    """
    precision = 10e-5
    def __init__(self,dt=0.1,expectedNbCluster=1,**kwargs):
        MapND.__init__(self,size=1,name="Scenario1",dt=dt)
        self.nbIteration = 0
        self.convergence = None
        self.time = 0
        self.processorTime = time.clock()
        self.expectedNbCluster = expectedNbCluster

    def getRoot(self):
            return self



    def reset(self):
        MapND.reset(self)
        self.nbIteration = 0
        self.time = 0
        self.convergence = None
        self.processorTime = time.clock()
        


    def initStats(self):
        """
        Init the stats and return it
        """
        return StatsTracking(self.runner)



    def applyContext(self,runner):
        """
        If we need to change parameters of the model
        """
        self.runner = runner

    def isTime(self,time):
        return abs(self.time -  time) <= self.precision



    def compute(self,time):
        self.nbIteration += 1
        #Not general enough######################
        self.trackedTargets = self.runner.getMap("trackedTargets")
        #print("time : %s"%simuTime)
        #print("coherency time :%s"% trackedTargets.isFreezed())
        if not(self.convergence) and trackedTargets.isFreezed():
            self.convergence = time - trackedTargets.getArg("coherencyTime")

        model.getMap("clusterMap").setParams(expectedNumberOfCluster=self.expectedNbCluster)
        #############################################
        self._apply(time)

    def _apply(self,time):
        pass


    def finalize(self):
        """
        Do something when simulation ends
        and return information
        """

        endProcessorTime = time.clock()


        clusterMap = self.runner.getMap("clusterMap")

        error = self.runner.getMap("errorDist").getArg("mean")
        nbClusterSum = clusterMap.getArg("nbClusterSum")
        wellClusterized = nbClusterSum/float(self.nbIteration)
        maxNbAct =clusterMap.getMaxNbAct()
        meanNbAct = clusterMap.getMeanNbAct()
        elapsedTime = endProcessorTime - self.processorTime
        errorShape  = self.runner.getMap("errorShape").getArg("mean")
        compEmpty = clusterMap.getArg("nbComputationEmpty")/float(self.nbIteration)
        nbClusterEnd = len(clusterMap.getData())
        if (clusterMap.nbActivation == 0 or clusterMap.getData()[0][0] == -1 ):
                nbClusterEnd = 0
       
        diffNbClustSum = clusterMap.diffNbClusterSum/(self.time/clusterMap.getArg('dt'))
        #print("compEmpty %s, nbCom %s ,it %s"%(compEmpty,model.getMap("clusterMap").getArg("nbComputationEmpty"),float(self.nbIteration)))
        
        #return dict(error=error,wellClusterized=wellClusterized,time=self.time,conv=self.convergence,maxNbAct=maxNbAct,meanNbAct=meanNbAct,elapsedTime=elapsedTime,errorShape=errorShape,compEmpty=compEmpty,nbClusterEnd=nbClusterEnd,diffNbClustSum=diffNbClustSum)
        return (error,wellClusterized,self.time,self.convergence,maxNbAct,meanNbAct,elapsedTime,errorShape,compEmpty,nbClusterEnd,diffNbClustSum)


    def __str__(self):
            return str(self.__class__).split("'")[-2].split(".")[-1]

    @staticmethod
    def getCharacNameList():
        return ["ErrorDist","WellClusterized","timeEnd","convergenceTime","maxNbAct","meanNbAct","elapsedTime","ErrorShape","CompEmpty"]

