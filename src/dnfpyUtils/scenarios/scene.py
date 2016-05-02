import numpy as np
from dnfpyUtils.scenarios.scenario import Scenario
from dnfpy.model.inputMap1D import InputMap

class Scene(Scenario):
    """
    Scene to be explored
    """
    def initMaps(self,size=49,dim=2,dt=0.1,iStim1=1.0,iStim2=0.95,wrap=True,trackSpeed=0.04,mapUnderStats="",**kwargs):
        self.trackSpeed = trackSpeed
        self.input = InputMap("Inputs",size,dt=dt,dim=dim,wrap=wrap,straight=True,speed=0.0,
                iStims=[1.,0.95],position=[[0.2,0.2],[0.2,0.45]],noiseI=0.3,thDVS=0.7,nbDistr=0,distr_dt=1.0,iDistr=1.0,**kwargs)

        self.mapUnderStats = mapUnderStats #change the expected target accordingly
        self.dim = dim
        self.track0,self.track1 = self.input.getTracks()
        self.targetList = None
        self.iStim1 = iStim1
        self.iStim2 = iStim2

        return [self.input,]

    def applyContext(self):
        super().applyContext()
        self.track0.setParamsRec(speed=0.0)
        self.track0.setParams(intensity=self.iStim1)
        self.track1.setParamsRec(speed=0.0)
        self.track1.setParams(intensity=self.iStim2)
        self.track1.setParamsRec(start=np.array((0.5,)*self.dim))
        if self.runner.isPresent("stats"):
            try:
                self.targetList = self.runner.getMap("TargetList")
                self.targetList.setData([0,])
            except:
                print("targetList not found")

    def reset(self):
        super().reset()

        
    def _apply(self,):
        if self.isTime(12.0):
            self.track0.setParamsRec(speed=self.trackSpeed,direction=[1,0])
            self.track1.setParamsRec(speed=self.trackSpeed/2)
        elif self.isTime(30.0):
            self.track0.setParamsRec(speed=0.0)
            self.track1.setParamsRec(speed=0.0)



        



