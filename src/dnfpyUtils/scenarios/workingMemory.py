
from dnfpyUtils.scenarios.scenario import Scenario
from dnfpy.model.inputMap1D import InputMap

class WorkingMemory(Scenario):
    """
    From FIX 2011

    Two static tracks from 0 to 40
    Intensity : 
        track0 0.3 then at 10s 1 then 15 0.3
        track0 0.3 then at 30s 1 then 35 0.3
    Width = 0.1




    """
    def initMaps(self,size=49,dim=2,dt=0.1,noiseI=0.1,nbDistr=2, **kwargs):
        self.iLow = 0.3
        self.iHigh = 1.0
        self.input = InputMap("Inputs",size,dt=dt,dim=dim,
                periodStim=100000,iStim1=self.iLow,iStim2=self.iLow,noiseI=noiseI,nbDistr=nbDistr,distr_dt=0.5)

        self.track0,self.track1 = self.input.getTracks()

        return [self.input,]

    def applyContext(self):
        super().applyContext()
        if self.runner.isPresent("stats"):
            try:
                self.targetList = self.runner.getMap("TargetList")
                self.targetList.setData([])
            except:
                print("targetList not found")


        
    def _apply(self,):
        if self.isTime(10.0):
            self.track0.setParams(intensity=self.iHigh)
            if self.targetList:
                self.targetList.setData([0,])
        elif self.isTime(15.0):
            self.track0.setParams(intensity=self.iLow)
        elif self.isTime(25.0):
            self.track1.setParams(intensity=self.iHigh)
            if self.targetList:
                self.targetList.setData([0,1])
        elif self.isTime(30.0):
            self.track1.setParams(intensity=self.iLow)


        



