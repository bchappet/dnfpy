from dnfpyUtils.scenarios.scenario import Scenario
class ScenarioStatic(Scenario):
    def __init__(self,timeStim=1.5,**kwargs):
        super(ScenarioStatic,self).__init__(**kwargs)
        self.timeStim = timeStim

    def applyContext(self):
        """
        If we need to change parameters before modele instanciation
        """
        super().applyContext()
        model = self.runner
        period=10e-10 #the target should not move
        radius = 0
        traj1X = model.getMap("Inputs_track0_c0")
        traj1X.setParams(period=period)
        traj1X.setParams(radius=radius)
        traj1Y = model.getMap("Inputs_track0_c1")
        traj1Y.setParams(period=period)
        traj1Y.setParams(radius=radius)

        traj2X = model.getMap("Inputs_track1_c0")
        traj2X.setParams(period=period)
        traj2X.setParams(radius=radius)
        traj2Y = model.getMap("Inputs_track1_c1")
        traj2Y.setParams(period=period)
        traj2Y.setParams(radius=radius)

        self.track0 = model.getMap("Inputs_track0")
        self.track0.setParams(intensity=1.)

        self.track1 = model.getMap("Inputs_track1")
        self.track1.setParams(intensity=0.)

        #model.getMap("Inputs").setParamsRec(noiseI=0.)


    def _apply(self):
        if self.isTime(self.timeStim):
            self.track0.setParams(intensity=0.)






