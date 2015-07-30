from scenario import Scenario

class ScenarioSwitchWM(Scenario):
    def __init__(self):
        super(ScenarioSwitchWM,self).__init__()
        self.wrongNumberOfCluster = 0
        self.expectedNbCluster = 2
        self.tck_dt = 0.1

    def reset(self):
        super(ScenarioSwitchWM,self).reset()
        self.wrongNumberOfCluster = 0
        self.expectedNbCluster = 2


    def applyContext(self,model):
        """
        If we need to change parameters before modele instanciation
        """
        self.input = model.getMap("Inputs")
        self.input.setParamsRec(tck_dt=self.tck_dt)

        self.track0 = model.getMap("Inputs_track0")
        self.track1 = model.getMap("Inputs_track1")
        self.track0.setParams(intensity=1.)
        self.track1.setParams(intensity=1.)

    def _apply(self,model,time,runner):
        if self.isTime(12.0):
            self.track0.setParams(intensity=0.)
            self.track1.setParams(intensity=0.)
            self.input.setParamsRec(tck_dt=1e8)#the target should not move
            self.input.compute()
        else:
            pass

        nbCluster = len(model.getMap("clusterMap").getData())
        errorNbCluster =  abs(nbCluster - self.expectedNbCluster)
        self.wrongNumberOfCluster +=errorNbCluster

    def finalize(self,model,runner):
       (error,wellClusterized,self.time,self.convergence,maxNbAct,meanNbAct,elapsedTime,errorShape,compEmpty) = \
       super(ScenarioSwitchWM,self).finalize(model,runner)
       return  (error,wellClusterized,self.time,self.convergence,maxNbAct,meanNbAct,elapsedTime,errorShape,compEmpty,
                self.wrongNumberOfCluster/float(self.nbIteration))



