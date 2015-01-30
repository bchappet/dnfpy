from scenario import Scenario
class ScenarioControl(Scenario):

    def applyContext(self,model):
        model.getMap("Inputs").setParamsRec(noiseI=0,iStim1=1.)
