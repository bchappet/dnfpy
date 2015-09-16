import time
from dnfpy.controller.runnable import Runnable
from dnfpyUtils.stats.statsTracking import StatsTracking
from dnfpy.core.mapND import MapND
class Scenario(Runnable,MapND):
    """
    Mother class for every scenario
    TODO it is a bit to specific for dnf2D with tracking tasks
    The scenario initilize the statistics, change the execution context before starting(in apply context) or during the execution in _apply

    """
    precision = 10e-5
    def __init__(self,dt=0.1,**kwargs):
        MapND.__init__(self,size=1,name="Scenario",dt=dt,**kwargs)
        self.nbIteration = 0
        self.time = 0
        self.processorTime = time.clock()

        self.mapDict = {"scenario":self}

    def getRoot(self):
            return self



    def resetRunnable(self):
        MapND.reset(self)
        self.nbIteration = 0
        self.processorTime = time.clock()
        




    def init(self,runner):
        """
        If we need to change parameters of the model
        """
        self.runner = runner
        self._applyContext()

    def _applyContext(self):
        pass

    def isTime(self,time):
        currentTime = self.getArg('time')
        return abs(currentTime -  time) <= self.precision



    def _compute(self):
        self.nbIteration += 1
        self._apply()

    def _apply(self):
        pass


    def finalize(self):
        """
        Do something when simulation ends
        and return information
        """
        return []




    def __str__(self):
            return str(self.__class__).split("'")[-2].split(".")[-1]
