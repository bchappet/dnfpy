class Scenario(object):
    precision = 10e-5
    def __init__(self):
        self.nbIteration = 0
        self.convergence = None
        self.time = 0


    def reset(self):
        self.nbIteration = 0
        self.time = 0
        self.convergence = None


    def applyContext(self,model):
        """
        If we need to change parameters before modele instanciation
        """
        pass

    def isTime(self,time):
        return abs(self.time -  time) <= self.precision



    def apply(self,model,time,runner):
        self.nbIteration += 1
        self.time = time
        trackedTargets = model.getMap("trackedTargets")
        if not(self.convergence) and trackedTargets.isFreezed():
            self.convergence = time - trackedTargets.getArg("coherencyTime")


        self._apply(model,time,runner)

    def _apply(self,model,time,runner):
        pass


    def finalize(self,model,runner):
        """
        Do something when simulation ends
        and return information
        """
        error = model.getMap("errorDist").getArg("mean")
        nbClusterSum = model.getMap("clusterMap").getArg("nbClusterSum")
        wellClusterized = nbClusterSum/float(self.nbIteration)
        return (error,wellClusterized,self.time,self.convergence)

    @staticmethod
    def getCharacNameList():
        return ["ErrorDist","WellClusterized","timeEnd","convergenceTime"]
