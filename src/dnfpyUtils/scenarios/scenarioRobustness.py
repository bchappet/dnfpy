from dnfpyUtils.scenarios.scenarioTracking import ScenarioTracking
class ScenarioRobustness(ScenarioTracking):
    def __init__(self,noiseI=0.5,nbDistr=3,distr_dt=1.0,**kwargs):
        super().__init__(**kwargs)
        self.noiseI = noiseI
        self.nbDistr = nbDistr
        self.distr_dt = distr_dt


    def _apply(self):
       super()._apply()
       if self.isTime(2.0):
            self.runner.getMap("Inputs").setParamsRec(
                noiseI=self.noiseI,nbDistr=self.nbDistr,distr_dt=self.distr_dt)
