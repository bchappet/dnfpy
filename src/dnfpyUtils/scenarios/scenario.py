import time
from dnfpy.model.inputMap1D import InputMap
from dnfpy.controller.runnable import Runnable
from dnfpyUtils.stats.statsTracking import StatsTracking
from dnfpy.core.mapND import MapND
class Scenario(Runnable,MapND):
    """
    Abstract class for every scenario
    TODO it is a bit to specific for dnf2D with tracking tasks
    The scenario initilize the statistics, change the execution context before starting(in apply context) or during the execution in _apply

    """
    precision = 10e-5
    def __init__(self,**kwargs):
        MapND.__init__(self,name="Scenario",**kwargs)
        self.nbIteration = 0
        self.time = 0
        self.processorTime = time.clock()

        self.mapDict = {"scenario":self}
        self.kwargs = kwargs #save for initialization

    def init(self,runner):
        self.runner = runner
        self.root = self.initMaps(**self.kwargs)
        self._addMapsToDict(self.root) #recursively add map to mapDict




    def getRoot(self):
            return self

    def getMapDict(self):
            return self.mapDict


    def resetRunnable(self):
        super().resetRunnable()
        self.nbIteration = 0
        self.processorTime = time.clock()
        


    def applyContext(self):
        """
        When everything is constructed or when reset
        """
        model = self.runner.getRunnable("model")
        model.onAfferentMapChange(self.input)


    def getArrays(self):
        return [self.input,]



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
        for map in self.mapDict.values():
            map.close()
        return []

    def onClick(self,mapName,x,y):
        pass




    def __str__(self):
            return str(self.__class__).split("'")[-2].split(".")[-1]
