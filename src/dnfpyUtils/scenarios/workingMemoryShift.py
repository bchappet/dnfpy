
from dnfpyUtils.scenarios.scenario import Scenario
from dnfpy.model.inputMap1D import InputMap

class WorkingMemoryShift(Scenario):
    """
    The working memory is optimised in a scene exploration framework ie

    Transient stimulis iHigh should trigger an autoactivated bubble as fast as possible
    The bubble sould follow the stimulus afterward even if there are moving
    The input distracters should be weak (not more than iLow)
    But should desapear if intensityLow disapears




    """
    def initMaps(self,size=49,dim=2,dt=0.1,wrap=True,trackSpeed=0.04,iLow=0.3,iHigh=1.0,**kwargs):
        self.iLow = iLow
        self.iHigh = iHigh
        self.trackSpeed = trackSpeed
        self.input = InputMap("Inputs",size,dt=dt,dim=dim,wrap=wrap,straight=True,speed=0.0,
                iStim1=self.iLow,iStim2=self.iLow,noiseI=0.01,nbDistr=0,distr_dt=1.0,iDistr=iLow)

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
        if self.isTime(6.0):
            self.track0.setParams(intensity=self.iHigh)
            self.track1.setParams(intensity=self.iHigh)
            if self.targetList:
                self.targetList.setData([0,1])
        if self.isTime(7.0):
            self.track0.setParams(intensity=self.iLow)
            self.track1.setParams(intensity=self.iLow)
        elif self.isTime(12.0):
            self.track0.setParamsRec(speed=self.trackSpeed,direction=[1,0])
            self.track1.setParamsRec(speed=self.trackSpeed/2)
        elif self.isTime(30.0):
            self.track0.setParamsRec(speed=0.0)
            self.track1.setParamsRec(speed=0.0)
        elif self.isTime(35.0):
            self.track0.setParams(intensity=0.0)
            self.track1.setParams(intensity=0.0)
        elif self.isTime(35.5):#give 0.5 sec to remove act
            if self.targetList:
                self.targetList.setData([])



        



