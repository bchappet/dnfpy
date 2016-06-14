from dnfpyUtils.scenarios.scenarioTracking import ScenarioTracking
class ScenarioNoise(ScenarioTracking):
    def __init__(self,noiseI=0.75,**kwargs):
        super().__init__(**kwargs)
        self.noiseI=noiseI

    def applyContext(self):
        super().applyContext()
        self.input.setParamsRec(
                noiseI=0.01,nbDistr=0)



    def _apply(self):
       if self.isTime(2.0):
            self.input.setParamsRec(noiseI=self.noiseI)


