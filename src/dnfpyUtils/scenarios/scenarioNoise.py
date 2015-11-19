from dnfpyUtils.scenarios.scenarioTracking import ScenarioTracking
class ScenarioNoise(ScenarioTracking):
    def __init__(self,noiseI=0.75,**kwargs):
        super().__init__(**kwargs)
        self.noiseI=noiseI


    def _apply(self):
       if self.isTime(2.0):
            self.runner.getMap("Inputs").setParamsRec(noiseI=self.noiseI)


    def resetRunnable(self):
            super().resetRunnable()
            self.runner.getMap("Inputs").resetParams()
