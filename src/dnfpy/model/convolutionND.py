from dnfpy.core.mapND import MapND
import numpy as np
import cv2
import scipy.ndimage.filters as filter

class ConvolutionND(MapND):
    """
        Perform a FFT convolution
        Expected parameters:
            source
            kernel
            wrap

    """
    def __init__(self,name,size,dt=0.1,wrap=True,kernelProjection=0,**kwargs):
        super(ConvolutionND,self).__init__(name,size=size,dt=dt,wrap=wrap,
                                         **kwargs)

    def _compute(self,source,size,kernel,wrap):
        if wrap:
            border = 'wrap'
        else:
            border = 'reflect'

        #self._data = cv2.filter2D(source,-1,cv2.flip(kernel,-1),
        #                          anchor=(-1,-1),borderType=border)
        self._data = filter.convolve(source,kernel,mode=border)
