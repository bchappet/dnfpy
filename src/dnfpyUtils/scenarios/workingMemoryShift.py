
from dnfpyUtils.scenarios.scenario import Scenario
from dnfpy.model.inputMap1D import InputMap

class WorkingMemoryShift(Scenario):
    """
    From FIX 2013

    One static tracks from 10 to 40
    one shifting track form 25 to 40
    Intensity : 
        track0 0.3 then at 10s 1 then 15 0.3
        track0 0.3 then at 30s 1 then 35 0.3
    Width = 0.1




    """
    def initMaps(self,size=49,dim=2,dt=0.1,wrap=True,**kwargs):
        self.iLow = 0.3
        self.iHigh = 1.0
        self.input = InputMap("Inputs",size,dt=dt,dim=dim,wrap=wrap,straight=True,speed=0.0,
                iStim1=self.iLow,iStim2=self.iLow,noiseI=0.01,nbDistr=0,distr_dt=0.5)

        self.track0,self.track1 = self.input.getTracks()

        return [self.input,]

    def applyContext(self):
        super().applyContext()
        if self.runner.isPresent("stats"):
            self.targetList = self.runner.getMap("TargetList")
            self.targetList.setData([])

    def reset(self):
        super().reset()

        
    def _apply(self,):
        if self.isTime(1.0):
            self.track0.setParams(intensity=self.iHigh)
            if self.runner.isPresent("stats"):
                self.targetList.setData([0,])
        elif self.isTime(5.0):
            self.track0.setParams(intensity=self.iLow)
        elif self.isTime(10.0):
            self.track1.setParams(intensity=self.iHigh)
            self.track1.setParamsRec(speed=0.02)
            if self.runner.isPresent("stats"):
                self.targetList.setData([0,1])
        elif self.isTime(20.0):
            self.track1.setParams(intensity=self.iLow)
        elif self.isTime(30.0):
            self.track1.setParamsRec(speed=0.0)


        



