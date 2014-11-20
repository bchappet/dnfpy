import numpy as np



class Map2D(object):
    """The Map2D will be updated when simuTime = self.time + self.dt
    The allowed precision for the time values is 1e-10"""

    def __init__(self,size,dt,rParams):
        """Init a 2D numpy array of shape (size,size) dtype float32"""
        
        self.size = size
        self.rParams = rParams
        self.data = np.zeros((size,size),dtype=np.float32)
        
        self.allowed_error = 1e-10 #allowed precision for time values
        self.time = 0
        self.dt = dt
        self.children = {} #dict of str:Map2D
        #Debug utilities
        self.nb_computation = 0
        
    
    def compute(self):
        """Abstract should call super
        Update the array using the childrens and rParams"""
        self.nb_computation += 1
        return None
        
    
    def modifyParams(self,params,rParams):
        """Abstarct Optional : 
        Whenever the parameter dictionary is changed (and on model initialisation)
        The rParams (for real params) are processed with this method recursively
        The syntax is : rParams['some_param'] = 2 * params['some_param'] + 1"""
        return None
        
    def getNextUpdateTime(self):
        """Return self.time + self.dt"""
        return self.time + self.dt
        
    def getSmallestNextUpdateTime(self):
        """Return the smallest NUT of self and the children (recursive)
        This should be call before each update to know the global minimal NUT"""
        minNUT = self.getNextUpdateTime()
        for child in self.children.values():
                childNUT = child.getSmallestNextUpdateTime()
                if childNUT < minNUT:
                        minNUT = childNUT
        
        return minNUT
    
        
        
        
    def update(self,simuTime):
        """Compute first the children and then self
        Computation occurs only if simuTime = Map2D.getNextUpdateTime"""
                
        selfNUT = self.getNextUpdateTime()
        assert( simuTime - selfNUT <= self.allowed_error), \
            "Simulation problem: %r has not been updated. %r < %r" % (self,selfNUT,simuTime)
        for child in self.children.values():
                child.update(simuTime)
        if abs(self.getNextUpdateTime() - simuTime) <= self.allowed_error :
                self.time = simuTime
                self.compute()
        return None
                        
        
    def getData(self):
        """Accessor return self.data"""
        return self.data
        
    def updateParams(self,rParams):
        """If the params are modified update here"""
        self.rParams = rParams
        for child in self.children.values():
                child.updateParams(self.rParams)
        return None
    
    def addChildren(self,childrenToAdd):
        """Add N children using dictionary"""
        self.children.update(childrenToAdd)
        return None
        
     

