from dnfpy.core.map2D import Map2D
import cv2

class Convolution(Map2D):
    """
        Perform a FFT convolution
        Expected parameters:
            source
            kernel
            wrap
    """
    def __init__(self,size,dt=0.1,wrap=True,**kwargs):
        super(Convolution,self).__init__(size=size,dt=dt,wrap=wrap,**kwargs)
    def _compute(self,source,kernel,wrap):
        if wrap:
            border = cv2.BORDER_WRAP
        else:
            border = cv2.BORDER_DEFAULT
        self._data = cv2.filter2D(source,-1,cv2.flip(kernel,-1),
                                  anchor=(-1,-1),borderType=border)
