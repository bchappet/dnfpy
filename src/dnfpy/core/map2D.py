import numpy as np
import sys
import math
from computable import Computable
import inspect


class Map2D(Computable):
    """
    The Map2D will be updated when simuTime = self.time + self.dt
    The allowed precision for the time values is 1e-10

    Attributes:
        'size': the data is of shape (size,size)
        'dt':  the update will be done every dt (second)
        'time': simulation time
        self._data: data accessible with self.getData()

    Methods:
        _compute: abstract define the beahaviour of the map here.
            Use any attribute or child in the method parameter
            Set self._data to finalize the computation

        _onParamUpdate: abstract called whenever self.setArg is called
            Use any attribute in the method parameters

        compute: compute the children state and the self state without updating
            self.time

        update(compTime): update the children a then self
            if compTime = self.__getNextUpdateTime

        getSmallestNextUpdateTime: get the smallest self.time + self.dt whithin
        self and the children

    """

    def __init__(self,name,size,**kwargs):
        super(Map2D,self).__init__(size=size,**kwargs)
        """Init a 2D numpy array of shape (size,size) dtype float32"""

        self.setArg(time=0.0) #last simulation time (in seconds) : it is updated just befor compute() call
        if not(self.hasArg('dtype')):
            self.setArg(dtype=np.float32)
        self.reset() #init self._data
        self.name = name
        self.__precision = 7 #allowed precision
        self.__children = {} #dict of str:Map2D: the children are computed before self

        #To avoid recursivity
        self.__lock =False #True when method already called

        self.__childrenParamsUpdateArgs = inspect.getargspec(\
                        self._childrenParamsUpdate)[0]
        self.__childrenParamsUpdateArgs.remove('self')


    def getName(self):
        return self.name


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
        return self.getArg('time') + self.getArg('dt')

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

    def compute(self):
        """
            Public
            Perform an artificial coputation step for the childre
            and self without updating dt
        """
        if not(self.__lock):
                self.__lock = True
                for child in self.__children.values():
                        child.compute()
                self.__computationStep()
                self.__lock = False
        else:
                pass

    def __computationStep(self):
        self.setArg(**self._getChildrenStates())
        self._compute_with_params()




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
            #assert( simuTime - selfNUT <= allowed_error), \
            #    "Simulation problem: %r has not been updated. %r < %r" % (self,selfNUT,simuTime)

            for child in self.__children.values():
                 child.update(simuTime)

            if abs(self.__getNextUpdateTime() - simuTime) <= allowed_error :
                 self.setArg(time= round(simuTime,self.__precision))
                 self.__computationStep()
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
    def getChildrenNames(self):
        """
            Public
            Return the children name set
        """
        return set(self.__children.viewkeys())

    def getChildren(self):
        return self.__children

    def getChild(self,name):
        return self.__children[name]

    def getAttributesNames(self):
        """
            Public
            Return the attributes name set
            the children are not considered as attributes
        """
        return  self._getDictionaryNames() - self.getChildrenNames()




    def getTime(self):
        """Accessor return self.time"""
        return self.getArg('time')

    def getData(self):
        """Accessor return self._data"""
        return self._data

    def addChildren(self,**kwargs):
        """
            Public
            Add N children using dictionary
        """
        self.__children.update(**kwargs)
        self._onAddChildren(**kwargs)
        self.childrenParamsUpdate()


    def childrenParamsUpdate(self):
            args =  self._subDictionary(self.__childrenParamsUpdateArgs)
            self._childrenParamsUpdate(**args)

    def _onAddChildren(self,**kwargs):
        """
        Called when children are added via add children
        kwargs contains the dictionary of children
        typical use is to add the given children to other children
        """
        pass

    def setParamsRec(self,**kwargs):
        self.setParams(**kwargs)
        if len(self.__children) > 0:
            self.childrenParamsUpdate()

    def _childrenParamsUpdate(self):
        pass


    def removeChild(self,childName):
        """
            Public
            Remove one child with the name childName
            Return: True if the argument was successfully removed
        """
        try:
            del self.__children[childName]
            return True
        except KeyError:
            return False

    def getChildrenCount(self):
        """
            Public
            Return the number of child
        """
        return len(self.__children)
    def reset(self):
        """Reset the data to 0"""
        size = self.getArg('size')
        dtype = self.getArg('dtype')
        if size == 1:
            self._data = 0.
        else:
            self._data = np.zeros((size,size),dtype=dtype)
    @staticmethod
    def __associateDict(aDict,bDict):
        """Association beteween aDict and bDict:
        {aKeys -> aVals} == {bKeys -> bVals} => {aKeys -> bVals}
        """
        newDict = dict((k,bDict[aDict[k]]) for k in aDict.keys()   )
        return newDict




