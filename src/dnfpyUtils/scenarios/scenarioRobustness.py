from scenario import Scenario
class ScenarioRobustness(Scenario):
    def __init__(self,noiseI=0.5,nbDistr=3):
        super(ScenarioRobustness,self).__init__()
        self.noiseI=noiseI
        self.nbDistr = nbDistr


    def _apply(self,model,time,runner):
        if self.isTime(1.0):
            model.getMap("Inputs").setParamsRec(
                noiseI=self.noiseI,nbDistr=self.nbDistr)
