import numpy as np
from dnfpyUtils.scenarios.scenario import Scenario
from dnfpy.model.inputMap1D import InputMap

class Dual(Scenario):
    """
    The working memory is optimised in a scene exploration framework ie

    Transient stimulis iHigh should trigger an autoactivated bubble as fast as possible
    The bubble sould follow the stimulus afterward even if there are moving
    The input distracters should be weak (not more than iLow)
    But should desapear if intensityLow disapears


    """
    def initMaps(self,size=49,dim=2,dt=0.1,wrap=True,trackSpeed=0.04,thDVS=0.8,nbTrack=4,**kwargs):
        self.trackSpeed = trackSpeed
        self.intensities = [1.0,0.9,0.95,0.87]
        self.positions = [[0.1,0.2],[0.1,0.4],[0.1,0.8],[0.8,0.45]]
        self.directions = [[1,0],[1.3,1],[0,-1],[-1,0]]
        self.speeds = [0.04,0.03,0.03,0.03]
        self.input = InputMap("Inputs",size,dt=dt,dim=dim,wrap=wrap,straight=True,speed=0.0,
                iStims=self.intensities,noiseI=0.1,nbDistr=0,distr_dt=1.0,iDistr=1.0,
                thDVS=thDVS,position=self.positions,nbTrack=nbTrack,**kwargs)
        self.focus = InputMap("Focus",size,dt=dt,dim=dim,wrap=wrap,straight=True,speed=0.0,
                iStims=[0.0,0.0,0.0,0.0],noiseI=0.1,nbDistr=0,distr_dt=1.0,iDistr=1.0,
                thDVS=thDVS,position=self.positions,nbTrack=nbTrack,**kwargs)

        self.targetList = None
        self.dim = dim

        return [self.input,self.focus]

    def getArrays(self):
        return [self.input,self.focus]

    def applyContext(self):
        model = self.runner.getRunnable("model")
        model.onAfferentMapChange(self.input,self.focus)
        if self.runner.isPresent("stats"):
            try:
                self.targetList = self.runner.getMap("TargetList")
                self.targetList.setData([])
            except Exception as e:
                print("targetList not found")
                raise e

    def reset(self):
        super().reset()
        
    def _apply(self,):
        if self.isTime(6.0):
            for track,i in zip(self.focus.getTracks(),self.intensities):
                track.setParams(intensity=i)
            if self.targetList:
                self.targetList.setData([0,1,2,3])
        if self.isTime(7.0):
            for track in self.focus.getTracks():
                track.setParams(intensity=0.0)
        elif self.isTime(12.0):
            tracks = self.input.getTracks()
            for i in range(len(tracks)):
                tracks[i].setParamsRec(speed=self.speeds[i],direction=self.directions[i])
        elif self.isTime(30.0):
            for track in self.input.getTracks():
                track.setParamsRec(speed=0.0)
        elif self.isTime(35.0):
            for track in self.input.getTracks():
                track.setParams(intensity=0.0)
        elif self.isTime(35.5):#give 0.5 sec to remove act
            if self.targetList:
                self.targetList.setData([])
