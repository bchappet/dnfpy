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

    def _compute(self,source,size,kernel,wrap,dim):

        if dim == 2:
            #if wrap: 
            #    self._data = utils.conv2(source,kernel)
            #else:
            #    self._data = signal.fftconvolve(source,kernel,mode='same')
            border = cv2.BORDER_WRAP if wrap else cv2.BORDER_CONSTANT
            self._data = cv2.filter2D(source,-1,cv2.flip(kernel,-1),anchor=(-1,-1),borderType=border)
        elif dim == 1:
            border = 'wrap' if wrap else 'reflect'
            self._data = filter.convolve(source,kernel,mode=border)
        else:
            raise Exception("Dim ",dim, " is not supported")
