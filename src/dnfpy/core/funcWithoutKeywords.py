from map2D import Map2D
from funcMap2D import FuncMap2D

class FuncWithoutKeywords(FuncMap2D):
    """To use with a function taking an undifined amount of args
    It can takes only children args
    To put constant arg: use addComputeArgs
    """

    def __init__(self,func,size,**kwargs):
        super(FuncWithoutKeywords,self).__init__(func,size,**kwargs)

    def addComputeArgs(self,*args):
        """
            Public
            add some arguments from to compute list
        """
        for k in args:
                self._computeArgs.append(k)



    def addChildren(self,**kwargs):
        super(FuncWithoutKeywords,self).addChildren(**kwargs)
        self._computeArgs += kwargs.keys()

    def _compute(self,**args):
        """
            Call the func with the good arguments
            We give a list
        """
        self._data = self._func(*args.values())

