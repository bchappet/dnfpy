from dnfpyUtils.scenarios.scenario import Scenario
from dnfpyUtils.camera.dvsMap import DvsMap
class ScenarioDVS128(Scenario):
    """

    """
    
    def initMaps(self,size=49,dim=2,dt=0.1,**kwargs):
        """
        Initialize the maps and return the roots
        """
        assert(dim == 2)
        assert(size == 127)
        self.input = DvsMap("Inputs",size,dt=dt)
        return [self.input,]

