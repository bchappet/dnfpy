
from dnfpyUtils.scenarios.scenario import Scenario
from dnfpy.model.inputMap1D import InputMap

class Competition(Scenario):
    """
    From FIX 2011

    Two static tracks from 0 to 20
    Intensity : 1.0 and 0.9
    Width = 0.1




    """
    def initMaps(self,size=49,dim=2,dt=0.1,**kwargs):
        self.input = InputMap("Inputs",size,dt=dt,dim=dim,
                periodStim=100000,iStim1=1.0,iStim2=0.9,noiseI=0.1)
        self.track0,self.track1 = self.input.getTracks()
        return [self.input,]
        
    def _apply(self,):
        if self.isTime(20.0):
            self.track0.setParams(intensity=0.)
            self.track1.setParams(intensity=0.)
            self.input.setParamsRec(tck_dt=1e8)#the target should not move
            self.input.compute()
            self.runner.getMap("SimpleShape").eraseShape()
        else:
            pass


        



