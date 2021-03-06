from dnfpyUtils.scenarios.scenario import Scenario
class ScenarioSwitch(Scenario):

    def applyContext(self):
        super().applyContext(self)
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
        self.track0.setParams(intensity=0.9)

        self.track1 = model.getMap("Inputs_track1")
        self.track1.setParams(intensity=1.)

    def _apply(self):
        if self.isTime(2.0):
            self.track1.setParams(intensity=0.)
            self.runner.getMap("trackedTargets").setParams(canSwitch=True)
        elif self.isTime(4.0):
            self.track1.setParams(intensity=1.)
        else:
            pass

