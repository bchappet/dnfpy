from dnfpy.model.webcamMap import WebcamMap
from dnfpy.model.opticalFlowToBGR import OpticalFlowToBGR
from dnfpy.model.playCamMap import PlayCamMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.imageColorSelection import ImageColorSelection
from dnfpy.model.mapDNF import MapDNF
from dnfpy.model.opticalFlowMap import OpticalFlowMap
from dnfpy.core.funcWithoutKeywords import FuncWithoutKeywords
import dnfpy.core.utils as utils
import colorsys
import  numpy as np
import cv2
from dnfpy.model.channelSelect import ChannelSelect
from dnfpy.model.flowDirectionSelect import FlowDirectionSelect


class ModelDNFDualCam_BG(Model,Renderable):

    def initMaps(self,size):
        self.size = size
        dt = 0.6
        # CREATE MAPS
        # 1st and 2nd webcam + possible perturbations 
        self.webcam1 = WebcamMap("Webcam1",size,dt=dt,numDevice=0)
        self.playcam1 = PlayCamMap("PlayCam1",size)
        self.webcam2 = WebcamMap("Webcam2",size,dt=dt,numDevice=0)
        self.playcam2 = PlayCamMap("PlayCam2",size)
        # 1st webcam basic filtering: HSV color (outputing V)
        self.color_select = ImageColorSelection("ColorSelect",size,dt=dt)
        # one neural field per webcam
        self.field1 = MapDNF("DNF1",size,model='spike',dt=dt)
        self.field2 = MapDNF("DNF2",size,model='spike',dt=dt)
        # computing optical flows from both maps, then translating into colors
        self.flow1 = OpticalFlowMap("OpticalFlow1",size,dt=dt)
        self.flow2 = OpticalFlowMap("OpticalFlow2",size,dt=dt)
        self.ofBGR1 = OpticalFlowToBGR("OFtoBGR1",size=size,dt=dt)
        self.ofBGR2 = OpticalFlowToBGR("OFtoBGR2",size=size,dt=dt)
        # extracting average optical flow (1st webcam) under spikes as BGR coding, then filtering optical flow of webcam 2 accordingly
        self.ofColor = FlowDirectionSelect("SelectDir",size=1,dt=dt,globalSize=size,
                                                sampleSize=0.07)
        self.color_select2 =  ImageColorSelection("OptFlowColorSelect",size,dt=dt,color='fullManu')
        # finally summing for webcam 2 the filtered color and the extracted optical flow (coded as color)
        self.aff2 = FuncWithoutKeywords(utils.sumArrays,"MixedModeInput",size,dt=dt)
        
        # LINK MAPS
        # from webcam 1 to DNF 1
        self.playcam1.addChildren(image=self.webcam1)
        self.color_select.addChildren(image=self.playcam1)
        self.field1.addChildren(aff=self.color_select)
        # from webcam 1 to the extraction under spikes of the selected motion direction
        self.flow1.addChildren(img=self.playcam1)
        self.ofBGR1.addChildren(opticalFlow=self.flow1)
        self.ofColor.addChildren(flowBGR=self.ofBGR1,colorDNFAct=self.field1.getActivation())
        # from webcam 2 to DNF 2, using the selected motion direction, and mixing with the color filtering
        self.playcam2.addChildren(image=self.webcam2)
        self.flow2.addChildren(img=self.playcam2)
        self.ofBGR2.addChildren(opticalFlow=self.flow2)
        self.color_select2.addChildren(image=self.ofBGR2,hsv=self.ofColor)
        self.aff2.addChildren(of=self.color_select2,col=self.color_select)
        self.field2.addChildren(aff=self.aff2)
        # compute the playCam to avoid some problems TODO fix
        self.playcam1.compute()
        self.playcam2.compute()


        #return the roots
        root = self.field2

        return root

    def getArrays(self):
        ret =  [
                self.playcam1,
                self.color_select,
                self.field1.getActivation(),
                self.ofBGR1,

     #           self.ofColor,

                self.playcam2,
                self.ofBGR2,
                self.color_select2,
                self.aff2,
                self.field2.getActivation()
        ]
        return ret

    def onClick(self,mapName,x,y):
        print mapName.__class__
        if mapName == "PlayCam1":
            bgr = self.playcam1.getData()
            
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


