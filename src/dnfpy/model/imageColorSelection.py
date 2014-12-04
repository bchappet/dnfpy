from dnfpy.core.map2D import Map2D
import numpy as np
import cv2
class ImageColorSelection(Map2D):
    """
    Parameter:
        dt  : real
        image : (size,size,3) array in BGR
        color : string in ('red','green','blue','gray')
        reverseColors : boolean

    """

    def _onParamsUpdate(self,color,thresh,lowHSV,highHSV):
        #HSV threshold

        if color == 'red':
                lowHSV[0] = 0 - thresh
                highHSV[0] = 0 + thresh
        elif color == 'blue':
                lowHSV[0] = 120 - thresh
                highHSV[0] = 120 + thresh
        elif color == 'green':
                lowHSV[0] = 60-thresh
                highHSV[0] = 60+thresh
        elif color == 'pink':
                lowHSV[0] = 120-thresh
                highHSV[0] = 120+thresh


        elif color == 'gray':
                pass
        else:
                raise ValueError("bad color : %s"%color)
        return dict(lowHSV=lowHSV,highHSV=highHSV)


    def _compute(self,image,color,reverseColors,lowHSV,highHSV):
        if color == 'gray':
                gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        else:
                array = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(array,lowHSV,highHSV)
                res = cv2.bitwise_and(array,array, mask= mask)
                gray = res[:,:,2]

        if reverseColors:
                gray = 255 -  gray
        self._data =  normalize(gray)

def normalize(array):
        """
            Normalize between 0-1
        """
        array = array.astype(np.float32)
        dmax = np.max(array)
        dmin = np.min(array)
        deltaVal = dmax - dmin
        if deltaVal != 0:
                return (array-dmin)/deltaVal
        elif dmax != 0:
                return array/dmax
        else:
                return array


