from map2D import Map2D
from funcMap2D import FuncMap2D

class FuncWithoutKeywords(FuncMap2D):
    """To use with a function taking an undifined amount of args
    It can takes only children args
    To put constant arg: use addComputeArgs
    """

    def __init__(self,func,name,size,dt=0.1,**kwargs):
        super(FuncWithoutKeywords,self).__init__(func,name,size,dt=dt,**kwargs)
        self._computeMapList = [] #map to use as arg must be child
        self.childrenStatesList = [] #data of children


    def addChildren(self,*kwargs):
        self._computeMapList += kwargs
        theDict = self.extractDictFromMaps(kwargs)
        super(FuncWithoutKeywords,self).addChildren(**theDict)

    def extractDictFromMaps(self,mapList):
        the_dict = {}
        for map in mapList:
            the_dict.update({map.getName():map})
        return the_dict


    def _compute_with_params(self):
        self._compute(self._childrenStatesList)
        self.nb_computation += 1
        self.last_computation_args = self._getChildrenStatesList
        self.last_computation_dictionary = self._computeMapList

    def _computationStep(self):
        self._childrenStatesList = self._getChildrenStatesList(self._computeMapList)
        self._compute_with_params()


    def _compute(self,args):
        self._data = self._func(args)

    def _getChildrenStatesList(self,mapList):
        return [map.getData() for map in mapList]

