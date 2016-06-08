from dnfpyUtils.scenarios.scenario import Scenario
from dnfpyUtils.camera.aedatReader import AEDatReader
class ScenarioAEFile128(Scenario):
    """

    """
    
    def initMaps(self,file,size=49,dim=2,dt=0.1,offset=0,**kwargs):
        """
        Initialize the maps and return the roots
        """
        assert(dim == 2)
        assert(size == 127)
        self.input = AEDatReader("Inputs",size=size,dt=dt,fileName=file,offset=offset)
        return [self.input,]

