from dnfpy.core.map2D import Map2D
import numpy as np
import cv2
class ImageColorSelection(Map2D):
    """
    Parameter:
        dt  : real
        image : (size,size,3) array in BGR
        color : string in ('red','green','blue','gray','manu')
        reverse : boolean

    """
    def __init__(self,name,size,dt=0.1,color='manu',thresh=10,reverse=False,
                 satLow=0,satHigh=255,colorVal=0,valLow=0,valHigh=255,
                 **kwargs):
        super(ImageColorSelection,self).__init__(name=name,
            size=size,dt=dt,color=color,thresh=thresh,reverse=reverse,
            satLow=satLow,satHigh=satHigh,colorVal=colorVal,valLow=valLow,valHigh=valHigh,
            **kwargs)

    def _onParamsUpdate(self,color,colorVal):
        #HSV threshold

        if color == 'red':
		colorVal = 0
        elif color == 'blue':
		colorVal = 120
        elif color == 'green':
		colorVal = 60
        elif color == 'pink':
		colorVal = 150
	elif color == 'manu':
		pass
        elif color == 'gray':
                pass
        else:
                raise ValueError("bad color : %s"%color)



        return dict(colorVal=colorVal)


    def _compute(self,image,color,reverse,colorVal,thresh,satLow,satHigh,valHigh,valLow):
        if color == 'gray':
                gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        else:
		lowHSV = np.array([colorVal-thresh,satLow,valLow])
		highHSV = np.array([colorVal+thresh,satHigh,valHigh])
                array = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(array,lowHSV,highHSV)
                res = cv2.bitwise_and(array,array, mask= mask)
                gray = res[:,:,2]

        if reverse:
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


