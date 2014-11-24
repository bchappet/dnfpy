import numpy as np
import sys
import math
from computable import Computable


class Map2D(Computable):
    """
    The Map2D will be updated when simuTime = self.time + self.dt
    The allowed precision for the time values is 1e-10
    
    Construction arguments:
        'size':   the data will be np.array of shape (size,size)
                or a double if size = 1
        'dt':  the update will be done every dt (second)

    Attributes:
        'size': the data is of shape (size,size)
        'time': simulation time
        self._data: data accessible with self.getData()


    """

    def __init__(self,size,**kwargs):
        super(Map2D,self).__init__(size=size,**kwargs)
        """Init a 2D numpy array of shape (size,size) dtype float32"""
        
        self._setArg(time=0.0) #last simulation time (in seconds) : it is updated just befor compute() call
        self.reset() #init self._data
        self.__precision = 7 #allowed precision
        self.__children = {} #dict of str:Map2D: the children are computed before self
        self.__paramDict = {} #association compute keyword, global params key words

        #To avoid recursivity
        self.__lock =False #True when method already called


        
    
    def _compute(self):
        """
            Abstract
            Update self._data using all parameter of self.__dictionary
        """
        return None
        
        
    def __getNextUpdateTime(self):
        """
            Return self.time + self.dt
        """
        return self._getArg('time') + self._getArg('dt')
        
    def getSmallestNextUpdateTime(self):
        """
            Return the smallest NUT of self and the children(recursive)
            This should be call before each update to know 
            the global minimal NUT
            Recursif
        """
        if not(self.__lock):
            self.__lock = True
            minNUT = self.__getNextUpdateTime()
            for child in self.__children.values():
                    childNUT = child.getSmallestNextUpdateTime()
                    if childNUT < minNUT:
                            minNUT = childNUT
        
            self.__lock = False
            return minNUT
        else:
            return sys.maxint
    
        
    def update(self,simuTime):
        """
            Public, Final, Recursif
            Compute first the children and then self
            Computation occurs <==> simuTime = Map2D.getNextUpdateTime
        """

        if not(self.__lock):
            self.__lock = True
            selfNUT = self.__getNextUpdateTime()
            allowed_error = math.pow(10,-self.__precision)
            assert( simuTime - selfNUT <= allowed_error), \
                "Simulation problem: %r has not been updated. %r < %r" % (self,selfNUT,simuTime)
            
            for child in self.__children.values():
                 child.update(simuTime)

            if abs(self.__getNextUpdateTime() - simuTime) <= allowed_error :
                 self._setArg(time= round(simuTime,self.__precision))
#                print("time %f : compute %s"%(self.time,self))
                 #Update self.__dictionary with children vals
                 self._setArg(**self._getChildrenStates())
                 self._compute_with_params()
#                print("result : %s " %self._data)
            self.__lock = False
        else:
                pass
        return None
    def _getChildrenStates(self):
        """
            Protected
            Return a dict with child name -> data
        """
        newDict = {k:self.__children[k].getData() for k in self.__children.keys()}
        return newDict


                        
    def getTime(self):
        """Accessor return self.time"""
        return self._getArg('time')
        
    def getData(self):
        """Accessor return self._data"""
        return self._data

    def _modifyParams(self,params,globalParams):
        """
            Abstract Optional : 
            Mofify the params taken from globalParams
            for there final value to be in self.__dictionary
        """
        return params
    def registerOnGlobalParamsChange(self,**kwargs):
        """
            Public
            Init the self.__paramDict with **kwargs
            But does not add them to self.__dictionary
            One has to call self.updateParams for that

        """
        self.__paramDict = dict(**kwargs)

    def __updateParams(self,globalParams):
        """
            Private
            update self.__dictionary with a modification
            of the globalParams chosen by self.__paramDict
        """
        params = Map2D.__associateDict(self.__paramDict,globalParams)
        params = self._modifyParams(params,globalParams)
        self._setArg(**params)
        self._onParamUpdate()
    def _onParamUpdate(self):
        """
            Protected Abstract
            To be overiden to react on param update
        """


        
    def updateParams(self,globalParams):
        """
            Public, Final, Recursif
            If the globalParams are mofified, there should be updated
        """
        if not(self.__lock):
            self.__lock = True
            self.__updateParams(globalParams)
            for child in self.__children.values():
                child.updateParams(globalParams)
            self.__lock = False
        else:
            pass
        return None
    
    def addChildren(self,**kwards):
        """
            Public 
            Add N children using dictionary
        """
        self.__children.update(**kwards)
        self._setArg(**self.__children)


    def removeChild(self,childName):
        """
            Public
            Remove one child with the name childName
            Return: True if the argument was successfully removed
        """
        self._rmArg(childName)

    def getChildrenCount(self):
        """
            Public
            Return the number of child
        """
        return len(self.__children)
    def reset(self):
        """Reset the data to 0"""
        size = self._getArg('size')
        if size == 1:
            self._data = 0.
        else:
            self._data = np.zeros((size,size))
    @staticmethod
    def __associateDict(aDict,bDict):
        """Association beteween aDict and bDict:
        {aKeys -> aVals} == {bKeys -> bVals} => {aKeys -> bVals}
        """
        newDict = dict((k,bDict[aDict[k]]) for k in aDict.keys()   )
        return newDict
        
        
     

