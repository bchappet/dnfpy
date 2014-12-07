from dnfpy.model.webcamMap import WebcamMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.imageColorSelection import ImageColorSelection
from dnfpy.model.mapDNF import MapDNF
import colorsys
import  numpy as np
import cv2
from dnfpy.model.opticalFlowMap import OpticalFlowMap


class ModelDNFCamFlow(Model,Renderable):

    def initMaps(self,size):
        self.size = size
        dt = 0.5
        #Create maps
        self.webcam = WebcamMap("Webcam",size,dt=dt,numDevice=0)
        self.color_select = ImageColorSelection("ColorSelect",size,dt=dt,color='gray')
        self.flow = OpticalFlowMap("OpticalFlow",size,dt=dt)
        self.field = MapDNF("DNF",size,model='spike',dt=dt)
        #Link maps
        self.color_select.addChildren(image=self.webcam)
        self.flow.addChildren(img_gray=self.webcam)
        self.aff = self.flow
        self.field.addChildren(aff=self.aff)
        #return the root
        return self.field

    def getArrays(self):
        ret =  [
                self.webcam,
                self.color_select,
                self.flow,
                self.field
        ]
        ret.extend(self.field.getArrays())
        return ret

    def onClick(self,mapName,x,y):
            pass
