from dnfpy.core.map2D import Map2D
import numpy as np
import cv2
import matplotlib.pyplot as plt

class WebcamMap(Map2D):
    """ 
    Capture image from webcam
    Parameter:
        dt  : real
        color : string in ('red','green','blue','gray')
        reverseColors : boolean
            
    """
    def __init__(self,size,**kwargs):
        super(WebcamMap,self).__init__(size,**kwargs)
        self.capture = cv2.VideoCapture(0)


    def _onParamUpdate(self):
        #HSV threshold
        self.lowHSV = np.array([0,100,100])
        self.highHSV  = np.array([20,255,255])
        color = self._getArg('color')
        thresh = 50
        
        if color == 'red':  
                self.lowHSV[0] = 0 - thresh
                self.highHSV[0] = 0 + thresh
        elif color == 'blue':
                self.lowHSV[0] = 120 - thresh
                self.highHSV[0] = 120 + thresh
        elif color == 'green':
                self.lowHSV[0] = 60-thresh
                self.highHSV[0] = 60+thresh
        
        elif color == 'gray':
                pass
        else:
                raise ValueError("bad color : %s"%color)
        
                
        


    def _compute(self,size,color,reverseColors):
        ret,frame = self.capture.read()
        if color == 'gray':
                array = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                array = cv2.resize(array,(size,size))
        else:
                array = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
                array = cv2.inRange(array,self.lowHSV,self.highHSV)
                #print array.shape
                #array = array[:,:,2]

        array = cv2.resize(array,(size,size))
        if reverseColors:
                array = self.__invert(array)
        self._data =  self.__normalize(array)

    def __normalize(self,array):
        """
            Normalize between 0-1
        """
        array *= 1.0
        deltaVal = np.max(array) - np.min(array)
        if deltaVal != 0:
                return (array-np.min(array))/deltaVal
        elif np.max(array) != 0:
                return array/np.max(array)
        else:
                return array
    def __invert(sel,array):
        """
            Invert the colors
        """
        return 255 - array
