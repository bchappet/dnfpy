
from dnfpy.core.map2D import Map2D
import numpy as np
class GreedyConvolution(Map2D):
    """
    Perform a convolution with a different kernel for each cell
    _data contains the result of this "convolution"
    Children:
        source: the source activation sizexsize matrix
        lateralWeights: kernel for each cell sizexsize x size*size matrix


    """
    def __init__(self,name,size,dt=0.1,**kwargs):
        super(GreedyConvolution,self).__init__(name,size=size,dt=dt,**kwargs)

    def _compute(self,source,lateralWeights):
        self.__compute(source,lateralWeights)

    @profile
    def __compute(self,source,lateralWeights):
        (cols,rows) = source.shape
        for i in range(cols):
            for j in range(rows):
                self._data[i,j] = np.sum(source * lateralWeights[i,j])
