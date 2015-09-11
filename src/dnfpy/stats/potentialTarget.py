from dnfpy.core.map2D import Map2D
import numpy as np

class PotentialTarget(Map2D):
    def __init__(self,name,size=0,dt=0.1,sizeInput=20,**kwargs):
        super(PotentialTarget,self).__init__(name=name,size=size,dt=dt,
                sizeInput = sizeInput, **kwargs)

    def _compute(self):
        coords = []
        for target in self.input.getTracks():
            coords.append(np.array([target.getChild("centerX").getData(),
                          target.getChild("centerY").getData()]))

        self._data = np.array(coords)



    def _onAddChildren(self,**kwargs):
        """
        supose that the first child is the input
        """
        self.input = list(kwargs.values())[0]


