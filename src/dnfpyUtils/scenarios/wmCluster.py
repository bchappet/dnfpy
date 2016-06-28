import numpy as np
from dnfpyUtils.scenarios.scenario import Scenario
from dnfpy.model.inputMap1D import InputMap

class WmCluster(Scenario):
    """
    The working memory is optimised in a scene exploration framework ie

    Transient stimulis iHigh should trigger an autoactivated bubble as fast as possible
    The bubble sould follow the stimulus afterward even if there are moving
    The input distracters should be weak (not more than iLow)
    But should desapear if intensityLow disapears


    """
    def initMaps(self,size=49,dim=2,dt=0.1,wrap=False,trackSpeed=0.04,iLow=0.3,iHigh=1.0,
            nbDistr=0,noiseI=0.01,distr_dt=1.0,noise_dt=0.1,angle_traj = 0.3,
            **kwargs):
        self.angle_traj = angle_traj
        self.iLow = iLow
        self.iHigh = iHigh
        self.trackSpeed = trackSpeed
        self.noiseI=noiseI
        self.nbDistr = nbDistr
        self.input = InputMap("Inputs",size,dt=dt,dim=dim,wrap=wrap,straight=True,speed=0.0,
                iStims=[self.iLow,self.iLow],noiseI=0.01,nbDistr=0,distr_dt=distr_dt,iDistr=iLow,
                thDVS=0.4,position=[[0.1,0.15],[0.1,0.85]],bound=1.0,**kwargs)

        self.track0,self.track1 = self.input.getTracks()
        self.targetList = None
        self.dim = dim

        self.endShift = min(12 + 18*0.04/self.trackSpeed,30) if self.trackSpeed >0 else 30

        return [self.input,]

    def applyContext(self):
        super().applyContext()
        self.track0.setParams(intensity=self.iLow,position=[0.1,0.15],speed=0.0)
        self.track1.setParams(intensity=self.iLow,position=[0.1,0.85],speed=0.0)
        self.input.setParamsRec(noiseI=0.01,nbDistr=0,bound=1.0)


        if self.runner.isPresent("stats"):
            try:
                self.targetList = self.runner.getMap("TargetList")
                self.targetList.setData([])
                self.track1.setParamsRec(start=np.array((0.5,)*self.dim))
            except Exception as e:
                print("targetList not found")
                raise e

    def _apply(self,):
        if self.isTime(6.0):
            self.track0.setParams(intensity=self.iHigh)
            self.track1.setParams(intensity=self.iHigh)
            if self.targetList:
                self.targetList.setData([0,1])
        if self.isTime(7.0):
            self.track0.setParams(intensity=self.iLow)
            self.track1.setParams(intensity=self.iLow)
            self.input.setParamsRec(bound=self.iLow,nbDistr=self.nbDistr,noiseI=self.noiseI)
        elif self.isTime(12.0):
            self.track0.setParamsRec(speed=self.trackSpeed,direction=[1,self.angle_traj])
            self.track1.setParamsRec(speed=self.trackSpeed,direction=[1,-self.angle_traj])
        elif self.isTime(self.endShift):
            self.track0.setParamsRec(speed=0.0)
            self.track1.setParamsRec(speed=0.0)
        elif self.isTime(35.0):
            self.track0.setParams(intensity=0.0)
            self.track1.setParams(intensity=0.0)
        elif self.isTime(35.5):#give 0.5 sec to remove act
            if self.targetList:
                self.targetList.setData([])
