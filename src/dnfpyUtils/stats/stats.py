
from dnfpy.controller.runnable import Runnable



class Stats(Runnable):
    """
    Stats contains all the statistics maps
    If parameters or map are needed from the model we can fetch them
    in the runner.
    The scenario initilize the statistics, change the execution context before starting(in apply context) or during the execution in _apply
    """
    def __init__(self,**kwargs):
        self.mapDict = {}
        self.kwargs = kwargs #save for initialization

    def init(self,runner):
        self.runner = runner
        self.root = self.initMaps(**self.kwargs)
        self._addMapsToDict(self.root) #recursively add map to mapDict

    def initMaps(self,**kwargs):
        """
        Initialize the maps and return the roots
        """
        return []


    def applyContext(self):
        """
        Modify maps if needed
        Called after construction of the whole simulation and after each reset
        """
        pass

    def getRoot(self):
        return self.root

    def getMapDict(self):
        return self.mapDict

    def getArrays(self):
        """
        Return a list of stat map to display
        """
        return []
 




