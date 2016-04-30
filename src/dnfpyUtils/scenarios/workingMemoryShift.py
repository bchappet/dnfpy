
from dnfpyUtils.scenarios.scenario import Scenario
from dnfpy.model.inputMap1D import InputMap

class WorkingMemoryShift(Scenario):
    """
    One static tracks from 10 to 40
    one shifting track form 25 to 40
    Intensity : 
        track0 0.3 then at 10s 1 then 15 0.3
        track0 0.3 then at 30s 1 then 35 0.3
    Width = 0.1




    """
    def initMaps(self,size=49,dim=2,dt=0.1,wrap=True,trackSpeed=0.01,iLow=0.3,iHigh=1.0,**kwargs):
        self.iLow = iLow
        self.iHigh = iHigh
        self.trackSpeed = trackSpeed
        self.input = InputMap("Inputs",size,dt=dt,dim=dim,wrap=wrap,straight=True,speed=0.0,
                iStim1=self.iLow,iStim2=self.iLow,noiseI=0.1,nbDistr=1,distr_dt=1.0)

        self.track0,self.track1 = self.input.getTracks()
        self.targetList = None

        return [self.input,]

    def applyContext(self):
        super().applyContext()
        if self.runner.isPresent("stats"):
            try:
                self.targetList = self.runner.getMap("TargetList")
                self.targetList.setData([])
            except:
                print("targetList not found")

    def reset(self):
        super().reset()

        
    def _apply(self,):
        if self.isTime(1.0):
            self.track0.setParams(intensity=self.iHigh)
            if self.targetList:
                self.targetList.setData([0,])
        elif self.isTime(5.0):
            self.track0.setParams(intensity=self.iLow)
        elif self.isTime(10.0):
            self.track1.setParams(intensity=self.iHigh)
            self.track1.setParamsRec(speed=self.trackSpeed)
            if self.targetList:
                self.targetList.setData([0,1])
        elif self.isTime(20.0):
            self.track1.setParams(intensity=self.iLow)
        elif self.isTime(30.0):
            self.track1.setParamsRec(speed=0.0)


        



