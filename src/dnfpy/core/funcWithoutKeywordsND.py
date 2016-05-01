from dnfpy.core.mapND import MapND
from dnfpy.core.funcMapND import FuncMapND
from dnfpy.core.constantMapND import ConstantMapND

class FuncWithoutKeywords(FuncMapND):
    """To use with a function taking an undifined amount of args
    It can takes only children args
    To put constant arg: use addComputeArgs
    """

    def __init__(self,func,name,size,dt=0.1,paramList=[],**kwargs):
        """
        paramList : optional list which can be used by somme function

        """
        super(FuncWithoutKeywords,self).__init__(func,name,size,dt=dt,**kwargs)
        self._computeMapList = [] #map to use as arg must be child
        self.childrenStatesList = [] #data of children
        self.paramList = paramList


    def addChildren(self,*kwargs):
        """
        The arguments of func are the children
        """
        self._computeMapList += kwargs
        theDict = self.extractDictFromMaps(kwargs)
        super(FuncWithoutKeywords,self).addChildren(**theDict)

    def extractDictFromMaps(self,mapList):
        the_dict = {}
        for map in mapList:
            the_dict.update({map.getName():map})
        return the_dict


    def _compute_with_params(self):
        if len(self.paramList) > 0:
            param_state = self._subDictionary(self.paramList).values()
        else:
            param_state = None

        self._compute(self._childrenStatesList,param_state)
        self.nb_computation += 1
        self.last_computation_args = self._getChildrenStatesList
        self.last_computation_dictionary = self._computeMapList

    def _computationStep(self):
        self._childrenStatesList = self._getChildrenStatesList(self._computeMapList)
        self._compute_with_params()


    def _compute(self,args,params):
        if params:
            self._data = self._func(args,params)
        else:
            self._data = self._func(args)

    def _getChildrenStatesList(self,mapList):
        return [map.getData() for map in mapList]

    def addComputeArgs(self,*argNameList):
            for arg in argNameList:
                    self.addChildren(ConstantMapND(arg,1,self.getArg(arg)))


