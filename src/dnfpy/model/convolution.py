from dnfpy.core.map2D import Map2D
import numpy as np
import cv2

class Convolution(Map2D):
    """
        Perform a FFT convolution
        Expected parameters:
            source
            kernel
            wrap

    """
    def __init__(self,name,size,dt=0.1,wrap=True,kernelProjection=0,**kwargs):
        super(Convolution,self).__init__(name,size=size,dt=dt,wrap=wrap,
                                         **kwargs)

    def _compute(self,source,size,kernel,wrap):
        #TODO for reasons (opencv3) wrap does not work for kern size < 8
        border = cv2.BORDER_WRAP if wrap else cv2.BORDER_DEFAULT
        self._data = cv2.filter2D(source,-1,cv2.flip(kernel,-1),
                                  anchor=(-1,-1),borderType=border)
