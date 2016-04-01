import time
from dnfpy.controller.runnable import Runnable
from dnfpyUtils.stats.statsTracking import StatsTracking
from dnfpy.core.mapND import MapND
from dnfpyUtils.scenarios.scenario import Scenario
from dnfpy.model.inputMap1D import InputMap
class ScenarioTracking(Scenario):
    """

    """
    
    def initMaps(self,size=49,dim=2,dt=0.1,iStim1=1.0,iStim2=0.95,**kwargs):
        """
        Initialize the maps and return the roots
        """
        self.input = InputMap("Inputs",size,dt=dt,dim=dim,iStim1=iStim1,iStim2=iStim2,noise_dt=dt,tck_dt=dt)
        return [self.input,]

