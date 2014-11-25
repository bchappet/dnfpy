from map2D import Map2D
from funcMap2D import FuncMap2D

class FuncWithoutKeywords(FuncMap2D):
    """To use with a function taking an undifined amount of args
    It can takes only children args or a constant list"""
    def __init__(self,func,size,**kwargs):
        super(FuncWithoutKeywords,self).__init__(func,size,**kwargs)
        self._computeArgs += kwargs.keys()

    def registerOnGlobalParamsChange(self,**kwargs):
        super(FuncWithoutKeywords,self).registerOnGlobalParamsChange(**kwargs)
        self._computeArgs += kwargs.keys()

    def registerOnGlobalParamsChange_ignoreCompute(self,**kwargs):
        super(FuncWithoutKeywords,self).registerOnGlobalParamsChange(**kwargs)

    def ignoreComputeArgs(self,*args):
        """
            Public
            remove some arguments from the compute list
        """
        for k in args:
                self._computeArgs.remove(k)



    def addChildren(self,**kwargs):
        super(FuncWithoutKeywords,self).addChildren(**kwargs)
        self._computeArgs += kwargs.keys()

    def _compute(self,**args):
        """
            Call the func with the good arguments
            We give a list
        """
        self._data = self._func(*args.values())

