import numpy as np
from dnfpy.model.inputMap1D import InputMap
from dnfpyUtils.scenarios.scenario import Scenario

class Bifurcation(Scenario):
    def initMaps(self,size,dim=1,dt=0.1,wrap=True,distance=0.5,speed=0.04,**kwargs):
        self.input = InputMap("Inputs",size,dt=dt,dim=dim,wrap=wrap,straight=True,speed=speed,
                iStims=[1.0,1.0],position=[[0.5-distance/2,0.5],[0.5+distance/2,0.5]],
                direction=np.float32([[1,0],[-1,0]]),
                **kwargs)
        return [self.input,]

    def applyContext(self):
        super().applyContext()
        if self.runner.isPresent("stats"):
            try:
                self.targetList = self.runner.getMap("TargetList")
                self.targetList.setData([0,1])
            except Exception as e:
                print("targetList not found")
                raise e


