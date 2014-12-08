from dnfpy.model.webcamMap import WebcamMap
from dnfpy.model.playCamMap import PlayCamMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.imageColorSelection import ImageColorSelection
from dnfpy.model.mapDNF import MapDNF
import colorsys
import  numpy as np
import cv2


class ModelDNFCam(Model,Renderable):

    def initMaps(self,size):
        self.size = size
        dt = 0.5
        #Create maps
        self.webcam = WebcamMap("Webcam",size,dt=dt,numDevice=1)
        self.webcam.compute()
        self.playcam = PlayCamMap("PlayCam",size)
        self.playcam.addChildren(image=self.webcam)
        self.color_select = ImageColorSelection("ColorSelect",size,dt=dt)
        self.field = MapDNF("DNF",size,model='spike',dt=dt)
        #Link maps
        self.color_select.addChildren(image=self.playcam)
        self.aff = self.color_select
        self.field.addChildren(aff=self.aff)
        #return the root
        return self.field

    def getArrays(self):
        ret =  [
                self.playcam,
                self.aff,
                self.field
        ]
        ret.extend(self.field.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
        if mapName == "PlayCam":
            bgr = self.playcam.getData()
            
            sizeROI = self.size/10.
            s2 = round(sizeROI/2.)
            roi = bgr[y-s2:y+s2,x-s2:x+s2,:]
            hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
            colorVal = np.median(hsv[:,:,0])
            satHigh = np.max(hsv[:,:,1])
            satLow = np.min(hsv[:,:,1])
            valHigh = np.max(hsv[:,:,2])
            valLow = np.min(hsv[:,:,2])

            self.color_select.setArg(colorVal=colorVal,satLow=satLow,satHigh=satHigh)
            return "ColorSelect"


