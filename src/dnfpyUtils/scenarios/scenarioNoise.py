from scenario import Scenario
class ScenarioNoise(Scenario):
    def __init__(self,noiseI=0.75):
        super(ScenarioNoise,self).__init__()
        self.noiseI=noiseI


    def _apply(self,model,time,runner):
        if self.isTime(1.0):
            model.getMap("Inputs").setParamsRec(noiseI=self.noiseI)
