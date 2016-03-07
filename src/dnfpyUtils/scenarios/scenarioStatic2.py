from dnfpyUtils.scenarios.scenario import Scenario
class ScenarioStatic2(Scenario):
    def __init__(self,timeStim=2.,noiseI=0.5,**kwargs):
        super(ScenarioStatic2,self).__init__(expectedNbCluster=2,**kwargs)
        self.timeStim = timeStim
        self.noiseI = noiseI

    def applyContext(self):
        super().applyContext()
        model = self.runner
        self.input = model.getMap("Inputs")
        self.input.setParamsRec(noiseI=self.noiseI)

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
            self.runner.getMap("TargetList").setData([0,1])
        except(KeyError):
            pass

    def _apply(self):
        if self.isTime(self.timeStim):
            self.track0.setParams(intensity=0.)
            self.track1.setParams(intensity=0.)






