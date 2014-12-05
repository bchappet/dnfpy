from dnfpy.core.map2D import Map2D
import cv2

class WebcamMap(Map2D):
   """
       Capture image from webcam
   """
   def __init__(self,name,size,dt=0.1,numDevice=0,**kwargs):
        super(WebcamMap,self).__init__(name,size,dt=dt,numDevice=numDevice,**kwargs)
        self.capture = cv2.VideoCapture(numDevice)


   def _compute(self,size):
        ret,frame = self.capture.read()
        array = cv2.resize(frame,(size,size))
        self._data =  array

