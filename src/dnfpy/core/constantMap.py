from dnfpy.core.map2D import Map2D

class ConstantMap(Map2D):
    def __init__(self,name,size,value,**kwargs):
        super(ConstantMap,self).__init__(name,size,dt=1e10,value=value,**kwargs)

    def _compute(self,value):
        self._data = value



    def reset(self):
        super(ConstantMap,self).reset()
        self._data = self._init_kwargs['value']
