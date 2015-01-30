from dnfpy.model.webcamMap import WebcamMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.imageColorSelection import ImageColorSelection
from dnfpy.model.mapDNF import MapDNF
import colorsys
import  numpy as np
import cv2
from dnfpy.model.opticalFlowMap import OpticalFlowMap
from dnfpy.model.channelSelect import ChannelSelect
from dnfpy.core.funcMap2D import FuncMap2D
import dnfpy.core.utils as utils
from dnfpy.model.opticalFlowToBGR import OpticalFlowToBGR


class ModelDNFCamFlow(Model,Renderable):

    def initMaps(self,size):
        self.size = size
        dt = 0.5
        #Create maps
        self.webcam = WebcamMap("Webcam",size,dt=dt,numDevice=0)
        self.flow = OpticalFlowMap("OpticalFlow",size,dt=dt)
        self.channel = ChannelSelect("OFNorm",size,dt=dt,channel=0)
        self.abs = FuncMap2D(utils.abs,"OFIntensity",size,dt=dt)
        self.field = MapDNF("DNF",size,model='spike',dt=dt)
        self.test = OpticalFlowToBGR("test",size=size,dt=dt)
        #Link maps
        self.flow.addChildren(img=self.webcam)
        self.channel.addChildren(map=self.flow)
        self.abs.addChildren(x=self.channel)

        self.field.addChildren(aff=self.abs)

        self.test.addChildren(opticalFlow=self.flow)
        #return the root
        return [self.field,self.test]

    def getArrays(self):
        ret =  [
                self.webcam,
                self.abs,
                self.field,
                self.test,
        ]
        ret.extend(self.field.getArrays())
        return ret

    def onClick(self,mapName,x,y):
            pass
