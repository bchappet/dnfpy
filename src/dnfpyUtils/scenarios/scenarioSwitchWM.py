from dnfpyUtils.scenarios.scenario import Scenario

class ScenarioSwitchWM(Scenario):
    def __init__(self,noiseI=0.5):
        super(ScenarioSwitchWM,self).__init__()
        self.tck_dt = 0.1
        self.noiseI = noiseI



    def applyContext(self):
        """
        If we need to change parameters before modele instanciation
        """

        self.input = self.runner.getMap("Inputs")
        self.input.setParamsRec(tck_dt=self.tck_dt,noiseI=self.noiseI)
        

        self.track0 = self.runner.getMap("Inputs_track0")
        self.track1 = self.runner.getMap("Inputs_track1")
        self.track0.setParams(intensity=1.)
        self.track1.setParams(intensity=1.)


        try:
            self.runner.getMap("TargetList").setData([0,1])
        except(KeyError):
            pass

    def _apply(self,):
        if self.isTime(12.0):
            self.track0.setParams(intensity=0.)
            self.track1.setParams(intensity=0.)
            self.input.setParamsRec(tck_dt=1e8)#the target should not move
            self.input.compute()
        else:
            pass





