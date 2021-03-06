from dnfpyUtils.scenarios.scenarioTracking import ScenarioTracking
class ScenarioStatic(ScenarioTracking):
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

        for i in range(self.getArg('dim')):
            traj1X = model.getMap("Inputs_track0_c"+str(i))
            traj1X.setParams(period=period)
            traj1X.setParams(radius=radius)

            traj2X = model.getMap("Inputs_track1_c"+str(i))
            traj2X.setParams(period=period)
            traj2X.setParams(radius=radius)

        self.track0 = model.getMap("Inputs_track0")
        self.track0.setParams(intensity=1.)

        self.track1 = model.getMap("Inputs_track1")
        self.track1.setParams(intensity=0.)

        #model.getMap("Inputs").setParamsRec(noiseI=0.)


    def _apply(self):
        if self.isTime(self.timeStim):
            self.track0.setParams(intensity=0.)






