import numpy as np
import math


class Map2D(object):
    """The Map2D will be updated when simuTime = self.time + self.dt
    The allowed precision for the time values is 1e-10"""

    def __init__(self,size,dt,globalRealParams):
        """Init a 2D numpy array of shape (size,size) dtype float32"""
        
        self.size = size #size of the np.array shape
        self.time = 0 #last simulation time (in seconds) : it is updated just befor compute() call
        self.dt = dt #dt between to computation (in seconds)
        
        self.globalRealParams = globalRealParams #global parameters for computation
        self.reset() #init self.data

        
        self.precision = 7 #allowed precision
        self.children = {} #dict of str:Map2D: the children are computed before self
        
        #Debug utilities
        self.nb_computation = 0
        
    
    def compute(self):
        """Abstract should call super
        Update the array using the childrens and globalRealParams"""
        self.nb_computation += 1
        return None
        
    @staticmethod    
    def modifyParams(self,params,globalRealParams):
        """Abstarct Optional : 
        Whenever the parameter dictionary is changed (and on model initialisation)
        The globalRealParams (for real params) are processed with this method recursively
        The syntax is : globalRealParams['some_param'] = 2 * params['some_param'] + 1"""
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
        allowed_error = math.pow(10,-self.precision)
        assert( simuTime - selfNUT <= allowed_error), \
            "Simulation problem: %r has not been updated. %r < %r" % (self,selfNUT,simuTime)
            
        for child in self.children.values():
                child.update(simuTime)
        if abs(self.getNextUpdateTime() - simuTime) <= allowed_error :
                self.time = round(simuTime,self.precision)
               
                self.compute()
        return None
                        
    def getTime(self):
        """Accessor return self.time"""
        #print("selfTime %s " % self.time)
        return self.time
        
    def getData(self):
        """Accessor return self.data"""
        return self.data
        
    def updateParams(self,globalRealParams):
        """If the params are modified update here"""
        self.globalRealParams = globalRealParams
        for child in self.children.values():
                child.updateParams(self.globalRealParams)
        return None
    
    def addChildren(self,childrenToAdd):
        """Add N children using dictionary"""
        self.children.update(childrenToAdd)
        return None
    def reset(self):
        """Reset the data to 0"""
        if self.size == 1:
            self.data = 0.
        else:
            self.data = np.zeros((self.size,self.size))
        
     

