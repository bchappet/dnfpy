from dnfpyUtils.scenarios.scenarioTracking import ScenarioTracking
import numpy as np
class ScenarioStatic2(ScenarioTracking):
    def __init__(self,timeStim=1.5,**kwargs):
        super().__init__(**kwargs)
        self.timeStim = timeStim

    def applyContext(self):
        """
        If we need to change parameters before modele instanciation
        """
        super().applyContext()
        model = self.runner
        period=10e-10 #the target should not move
        traj1X = model.getMap("Inputs_track0_c0")
        traj1X.setParams(period=period)
        traj1Y = model.getMap("Inputs_track0_c1")
        traj1Y.setParams(period=period)

        traj2X = model.getMap("Inputs_track1_c0")
        traj2X.setParams(period=period)
        traj2Y = model.getMap("Inputs_track1_c1")
        traj2Y.setParams(period=period)

        self.track0 = model.getMap("Inputs_track0")
        self.track0.setParams(intensity=1.)

        self.track1 = model.getMap("Inputs_track1")
        self.track1.setParams(intensity=1.)

        try:
            model.getMap("TargetList").setData(np.array([0,1]))
        except:
            pass


    def _apply(self):
        pass
        #if self.isTime(self.timeStim):
        #    self.track0.setParams(intensity=0.)
        #    self.track1.setParams(intensity=0.)
