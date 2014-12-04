from dnfpy.core.map2D import Map2D
import dnfpy.core.utils as utils
import numpy as np


class OnOffFilter(Map2D):
    """
        One on cell in the center and two off cells
        Parameters :
            on cell stdXY, intXY
            off cells stdXY, intXY
            shift distance ( distance between center on gaussian and center off gaussian)
        TODO finish this class

    """

    def _compute(self,size,onIntXY,onStdXY,offIntXY,offStdXY,shift):
        onCell =  utils.getAssymetricGaussian2D(size,onIntXY,onStdXY)
        offCell1 =  utils.getAssymetricGaussian2D(size,offIntXY,offStdXY)
        offCell2 = np.array(offCell1)

        #for now it is a vertical edge detector TODO generalize
        offCell1 = np.roll(offCell1,-int(shift))
        offCell2 = np.roll(offCell2,int(shift))

        self._data =  onCell - (offCell1 + offCell2)

    def _onParamsUpdate(self,size,onStdXY,offStdXY,shift):
        onStdXY *= size
        offStdXY *= size
        shift *= size
        ret =  dict(onStdXY=onStdXY,offStdXY=offStdXY,shift=shift)
        return ret






