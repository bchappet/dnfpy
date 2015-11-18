from dnfpy.core.mapSpace import MapSpace
import inspect

class FuncMapSpace(MapSpace):
    def __init__(self,func,name,space,**kwargs):
        super().__init__(name,space,**kwargs)
        self._func = func #function to call at every computation
        #we have to modify self._computeArgs to fit the func
        self._computeArgs = inspect.getargspec(self._func)[0]
        if 'self' in self._computeArgs:
            self._computeArgs.remove('self')

    def _compute(self,**args):
        """Call the func with the good arguments"""
        self._data = self._func(**args)
