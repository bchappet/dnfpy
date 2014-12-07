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
        self.root.update(simuTime)

    def getSmallestNextUpdateTime(self):
        return self.root.getSmallestNextUpdateTime()

    def onclick(self,mapName,x,y):
        pass

    def __addMapsToDict(self,map):
        if not(map.getName() in self.mapDict.keys()):
            self.mapDict.update({map.getName():map})
        else:
            return
        childDic = map.getChildren()
        for child in childDic:
            self.__addMapsToDict(childDic[child])
