from dnfpyUtils.scenarios.scenarioTracking import ScenarioTracking

class ScenarioDistracters(ScenarioTracking):
    def __init__(self,nbDistr=4,**kwargs):
        super().__init__(**kwargs)
        self.nbDistr = nbDistr


    def _apply(self):
       if self.isTime(2.0):
            self.runner.getMap("Inputs").setParamsRec(nbDistr=self.nbDistr)
