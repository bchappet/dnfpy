from dnfpyUtils.scenarios.scenarioTracking import ScenarioTracking

class ScenarioDistracters(ScenarioTracking):
    def __init__(self,nbDistr=4):
        super(ScenarioDistracters,self).__init__()
        self.nbDistr = nbDistr


    def _apply(self):
       if self.isTime(1.0):
            self.runner.getMap("Inputs").setParamsRec(nbDistr=self.nbDistr)
