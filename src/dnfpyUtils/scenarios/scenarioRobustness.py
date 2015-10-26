from dnfpyUtils.scenarios.scenarioTracking import ScenarioTracking
class ScenarioRobustness(ScenarioTracking):
    def __init__(self,noiseI=0.5,nbDistr=3):
        super(ScenarioRobustness,self).__init__()
        self.noiseI=noiseI
        self.nbDistr = nbDistr


    def _apply(self):
       super()._apply()
       if self.isTime(1.0):
            self.runner.getMap("Inputs").setParamsRec(
                noiseI=self.noiseI,nbDistr=self.nbDistr)
