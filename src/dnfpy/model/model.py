class Model(object):
    """Abstract class for all the model"""

    def __init__(self,globalParams):
        self.globalParams = globalParams
        self.root = self.initMaps() #the root is the root map of the model
        #Update args
        self.root.updateParams(self.globalParams)

    def initMaps(self):
        """
            Abstract
            Construct and connect the maps
            return the root
        """
    def updateParams(self,params):
        self.root.updateParams(params)
    def update(self,simuTime):
        self.root.update(simuTime)
    
    def getSmallestNextUpdateTime(self):
        return self.root.getSmallestNextUpdateTime()
