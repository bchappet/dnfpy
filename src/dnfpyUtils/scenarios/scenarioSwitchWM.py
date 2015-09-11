from scenario import Scenario

class ScenarioSwitchWM(Scenario):
    def __init__(self,noiseI=0.5):
        super(ScenarioSwitchWM,self).__init__(expectedNbCluster=2)
        self.tck_dt = 0.1
        self.noiseI = noiseI

    def reset(self):
        super(ScenarioSwitchWM,self).reset()


    def applyContext(self,model):
        """
        If we need to change parameters before modele instanciation
        """
        self.input = model.getMap("Inputs")
        self.input.setParamsRec(tck_dt=self.tck_dt,noiseI=self.noiseI)
        

        self.track0 = model.getMap("Inputs_track0")
        self.track1 = model.getMap("Inputs_track1")
        self.track0.setParams(intensity=1.)
        self.track1.setParams(intensity=1.)

        model.getMap("clusterMap").setParams(clustSize=0.3)

    def _apply(self,model,time,runner):
        if self.isTime(12.0):
            self.track0.setParams(intensity=0.)
            self.track1.setParams(intensity=0.)
            self.input.setParamsRec(tck_dt=1e8)#the target should not move
            self.input.compute()
        else:
            pass





