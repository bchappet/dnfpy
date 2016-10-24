
from dnfpyUtils.scenarios.scenario import Scenario
from dnfpy.model.inputMap1D import InputMap

class WM1(Scenario):
    """

    One static track with intensity 1 diseaper after 5 seconds



    """
    def initMaps(self,size=49,dim=2,dt=0.1,noiseI=0.1,nbDistr=0, **kwargs):
        self.input = InputMap("Inputs",size,dt=dt,dim=dim,iStims=[1.0],straight=True,
                position=[(0.5,)*dim],nbTrack=1,speed=0.0,
                noiseI=noiseI,nbDistr=nbDistr,distr_dt=0.5)

        self.track0,= self.input.getTracks()

        return [self.input,]

    def applyContext(self):
        super().applyContext()
        if self.runner.isPresent("stats"):
            try:
                self.targetList = self.runner.getMap("TargetList")
                self.targetList.setData([0,])
            except:
                print("targetList not found")


        
    def _apply(self,):
        if self.isTime(5.0):
            self.track0.setParams(intensity=0.0)


        



