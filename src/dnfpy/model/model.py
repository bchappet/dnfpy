class Model(object):
    """Abstract class for all the model"""

    def __init__(self,size):
        self.root = self.initMaps(size) #the root is the root map of the model
        #Update args

    def initMaps(self):
        """
            Abstract
            Construct and connect the maps
            return the root
        """
    def updateParams(self,params):
        #TODO
        pass
    def update(self,simuTime):
        self.root.update(simuTime)

    def getSmallestNextUpdateTime(self):
        return self.root.getSmallestNextUpdateTime()
