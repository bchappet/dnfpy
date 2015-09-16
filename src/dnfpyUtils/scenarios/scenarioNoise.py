from dnfpyUtils.scenarios.scenarioTracking import ScenarioTracking
class ScenarioNoise(ScenarioTracking):
    def __init__(self,noiseI=0.75):
        super(ScenarioNoise,self).__init__()
        self.noiseI=noiseI


    def _apply(self):
       if self.isTime(1.0):
            self.runner.getMap("Inputs").setParamsRec(noiseI=self.noiseI)


    def resetRunnable(self):
            super().resetRunnable()
            self.runner.getMap("Inputs").resetParams()
