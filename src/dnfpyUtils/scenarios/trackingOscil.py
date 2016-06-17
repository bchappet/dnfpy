from dnfpy.model.inputMap1D import InputMap
from dnfpyUtils.scenarios.scenarioTracking import ScenarioTracking
class TrackingOscil(ScenarioTracking):
    def initMaps(self,size=49,dim=2,dt=0.1,**kwargs):
        """
        Initialize the maps and return the roots
        """
        self.input = InputMap("Inputs",size,dt=dt,dim=dim,nbTrack=1,noise_dt=dt,tck_dt=dt,oscil=True,
                **kwargs)
        return [self.input,]

