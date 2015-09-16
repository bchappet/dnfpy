from dnfpy.controller.runnable import Runnable
class Model(Runnable):
    """Abstract class for all the model"""

    def __init__(self,**kwargs):
        self.mapDict = {}
        self.root = self.initMaps(**kwargs) #the root is the root map of the model
        self._addMapsToDict(self.root) #recursively add map to mapDict


    def getRoot(self):
        return self.root



    def initMaps(self,size):
        """
            Abstract
            Construct and connect the maps
            return the root
        """

    def init(self,runner):
        """
        Nothing. part of Runnable interface
        """
        pass

    def getMap(self,mapName):
        map = self.mapDict[mapName]
        return map

    def getMapDict(self):
        return self.mapDict


    def firstComputation(self):
        """
        Compute map with dt infinite ie dt=1e10
        """
        for map in self.mapDict.values():
            if map.getArg('dt') == 1e10:
                map.compute()




