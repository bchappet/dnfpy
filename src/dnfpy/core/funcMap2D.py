from map2D import Map2D
import inspect

class FuncMap2D(Map2D):
    def __init__(self,func,name,size,**kwargs):
        super(FuncMap2D,self).__init__(name,size,**kwargs)
        self._func = func #function to call at every computation
        #we have to modify self._computeArgs to fit the func
        self._computeArgs = inspect.getargspec(self._func)[0]
        if 'self' in self._computeArgs:
            self._computeArgs.remove('self')

    def _compute(self,**args):
        """Call the func with the good arguments"""
        self._data = self._func(**args)
