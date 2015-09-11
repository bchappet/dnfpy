class Runnable(object):
    """
    Abstract class for runnable class
    A runnable can be given to the runner to update the maps when it is needed
    """


    def finalize(self):
        """
        return something when we end simulation
        """
        return None

    def initMaps(self,size):
        """
            Abstract
            Construct and connect the maps
            return the root
        """
    def getMapDict(self):
            return {}

    def getRoot(self):
            return None

    def updateParam(self,mapName,name,value):
        map = self.mapDict[unicode(mapName)]
        nameStr = unicode(name)
        map.setParamsRec(**{nameStr:value})


    def resetRunnable(self):
        for map in self.mapDict.values():
            map.reset()

    def firstComputation(self):
        """
        Compute map with dt infinite ie dt=1e10
        """
        for map in self.getMapDict().values():
            if map.getArg('dt') == 1e10:
                map.compute()




    def resetParamsRunnable(self):
        if isinstance(self.root,list):
            for root_i in self.root:
                root_i.resetParams()
        else:
            self.root.resetParams()




    def updateRunnable(self,simuTime):
        root = self.getRoot()
        if isinstance(root,list):
            for root_i in root:
                root_i.update(simuTime)
        else:
            root.update(simuTime)

    def getNextUpdateTime(self):
        root = self.getRoot()
        if isinstance(root,list):
            minTime = root[0].getSmallestNextUpdateTime()
            for root_i in root:
                if minTime > root_i.getSmallestNextUpdateTime():
                    minTime = root_i.getSmallestNextUpdateTime()
        else:
            minTime = root.getSmallestNextUpdateTime()
        return minTime

    def onclick(self,mapName,x,y):
        pass

    def onRClick(self,mapName,x,y):
        pass
    def _addMapsToDict(self,rootmap):
        if isinstance(rootmap,list):
            for root_i in rootmap:
                if not(root_i.getName() in self.mapDict.keys()):
                    self.mapDict.update({root_i.getName():root_i})
                else:
                    return
                childDic = root_i.getChildren()
                for child in childDic:
                    self._addMapsToDict(childDic[child])
        else:
            if not(rootmap.getName() in self.mapDict.keys()):
                self.mapDict.update({rootmap.getName():rootmap})
            else:
                return
            childDic = rootmap.getChildren()
            for child in childDic:
                self._addMapsToDict(childDic[child])


    def getName(self):
        return str(self)

    def __str__(self):
            return str(self.__class__).split("'")[-2].split(".")[-1]


