from dnfpyUtils.scenarios.scenario import Scenario
from dnfpy.model.inputMap1D import InputMap
class ScenarioControl(Scenario):
    def initMaps(self,size=49,dim=2,dt=0.1,**kwargs):
        """
        Initialize the maps and return the roots
        """
        self.input = InputMap("Inputs",size,dt=dt,dim=dim,iStim1=1.0,iStim2=0,noiseI=0)
        return [self.input,]


