from scenario import Scenario
class ScenarioDistracters(Scenario):
    def __init__(self,nbDistr=4):
        super(ScenarioDistracters,self).__init__()
        self.nbDistr = nbDistr


    def _apply(self,model,time,runner):
        if self.isTime(1.0):
            model.getMap("Inputs").setParamsRec(nbDistr=self.nbDistr)
