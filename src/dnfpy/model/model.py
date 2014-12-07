class Model(object):
    """Abstract class for all the model"""

    def __init__(self,size):
        self.mapDict = {}
        self.root = self.initMaps(size) #the root is the root map of the model
        self.__addMapsToDict(self.root)


    def initMaps(self):
        """
            Abstract
            Construct and connect the maps
            return the root
        """
    def updateParam(self,mapName,name,value):
        map = self.mapDict[unicode(mapName)]
        nameStr = unicode(name)
        map.setParamsRec(**{nameStr:value})


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

    def __addMapsToDict(self,rootmap):
        if isinstance(rootmap,list):
            for root_i in rootmap:
                if not(root_i.getName() in self.mapDict.keys()):
                    self.mapDict.update({root_i.getName():root_i})
                else:
                    return
                childDic = root_i.getChildren()
                for child in childDic:
                    self.__addMapsToDict(childDic[child])
        else:
            if not(rootmap.getName() in self.mapDict.keys()):
                self.mapDict.update({rootmap.getName():rootmap})
            else:
                return
            childDic = rootmap.getChildren()
            for child in childDic:
                self.__addMapsToDict(childDic[child])
