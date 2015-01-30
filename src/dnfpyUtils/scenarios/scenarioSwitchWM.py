from scenario import Scenario

class ScenarioSwitchWM(Scenario):
    def __init__(self):
        super(ScenarioSwitchWM,self).__init__()
        self.wrongNumberOfCluster = 0
        self.expectedNbCluster = 1

    def reset(self):
        super(ScenarioSwitchWM,self).reset()
        self.wrongNumberOfCluster = 0
        self.expectedNbCluster = 1


    def applyContext(self,model):
        """
        If we need to change parameters before modele instanciation
        """
        period=50 #the target should not move
        traj1X = model.getMap("Inputs_track0_cX")
        traj1X.setParams(period=period)
        traj1Y = model.getMap("Inputs_track0_cY")
        traj1Y.setParams(period=period)

        traj2X = model.getMap("Inputs_track1_cX")
        traj2X.setParams(period=period)
        traj2Y = model.getMap("Inputs_track1_cY")
        traj2Y.setParams(period=period)

        self.track0 = model.getMap("Inputs_track0")
        self.track0.setParams(intensity=0.9)

        self.track1 = model.getMap("Inputs_track1")
        self.track1.setParams(intensity=1.)

    def _apply(self,model,time,runner):
        if self.isTime(10.0):
            self.track1.setParams(intensity=0.)
            self.expectedNbCluster = 2
            #model.getMap("trackedTargets").setParams(canSwitch=True)
        elif self.isTime(15.0):
            self.track1.setParams(intensity=1.)
        else:
            pass

        nbCluster = len(model.getMap("clusterMap").getData())
        errorNbCluster =  abs(nbCluster - self.expectedNbCluster)
        self.wrongNumberOfCluster +=errorNbCluster

    def finalize(self,model,runner):
       (error,wellClusterized,self.time,self.convergence) = \
       super(ScenarioSwitchWM,self).finalize(model,runner)
       nbComputationEmpty = model.getMap("clusterMap").getArg("nbComputationEmpty")
       return  (error,wellClusterized,self.time,self.convergence,
                self.wrongNumberOfCluster/float(self.nbIteration),
                nbComputationEmpty/float(self.nbIteration))



