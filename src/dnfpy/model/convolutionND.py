from dnfpy.core.mapND import MapND
import numpy as np
import cv2
import scipy.ndimage.filters as filter
import dnfpy.core.utils as utils
from scipy import signal


class ConvolutionND(MapND):
    """
        Perform a FFT convolution
        Expected parameters:
            source
            kernel
            wrap

    """
    def __init__(self,name,size,dim=1,dt=0.1,wrap=True,kernelProjection=0,**kwargs):
        super(ConvolutionND,self).__init__(name,size=size,dim=dim,dt=dt,wrap=wrap,
                                         **kwargs)

    def _compute(self,source,kernel,wrap):
        self._data = utils.convolve(source,kernel,wrap)
