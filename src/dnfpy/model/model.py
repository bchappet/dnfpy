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
    def updateParam(self,mapName,name,value):
        map = self.mapDict[unicode(mapName)]
        nameStr = unicode(name)
        map.setParamsRec(**{nameStr:value})

    def getMap(self,mapName):
        map = self.mapDict[mapName]
        return map

    def getMapDict(self):
        return self.mapDict

    def reset(self):
        for map in self.mapDict.values():
            map.reset()

    def firstComputation(self):
        """
        Compute map with dt infinite ie dt=1e10
        """
        for map in self.mapDict.values():
            if map.getArg('dt') == 1e10:
                map.compute()




    def resetParams(self):
        if isinstance(self.root,list):
            for root_i in self.root:
                root_i.resetParams()
        else:
            self.root.resetParams()




    def update(self,simuTime):
        if isinstance(self.root,list):
            for root_i in self.root:
                root_i.update(simuTime)
        else:
            self.root.update(simuTime)

    def getSmallestNextUpdateTime(self):
        if isinstance(self.root,list):
            minTime = self.root[0].getSmallestNextUpdateTime()
            for root_i in self.root:
                if minTime > root_i.getSmallestNextUpdateTime():
                    minTime = root_i.getSmallestNextUpdateTime()
        else:
            minTime = self.root.getSmallestNextUpdateTime()
        return minTime

    def onclick(self,mapName,x,y):
        pass

    def onRClick(self,mapName,x,y):
        pass




