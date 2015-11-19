from dnfpyUtils.scenarios.scenario import Scenario
from dnfpy.model.inputMap1D import InputMap

class ScenarioSwitchWM(Scenario):

    def initMaps(self,size=49,dim=2,dt=0.1,noiseI=0.,**kwargs):
        self.input = InputMap("Inputs",size,dt=dt,dim=dim,
                periodStim=3000000,iStim1=1.0,iStim2=0.0,noiseI=noiseI,straight=True,speed=0.0)
        self.track0,self.track1 = self.input.getTracks()
        return [self.input,]


    def _apply(self,):
        if self.isTime(12.0):
            self.track0.setParams(intensity=0.)
            self.track1.setParams(intensity=0.)
            #self.input.setParamsRec(tck_dt=1e8)#the target should not move
            #self.input.compute()
        else:
            pass





