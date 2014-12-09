import cv2
import numpy as np
from dnfpy.core.funcMap2D import FuncMap2D
from dnfpy.model.inputMap import InputMap
from dnfpy.model.fieldMap import FieldMap
from dnfpy.model.activationMap import ActivationMap
from dnfpy.model.lateralWeightsMap import LateralWeightsMap
from dnfpy.model.webcamMap import WebcamMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.imageColorSelection import ImageColorSelection
from dnfpy.model.convolution import Convolution
import dnfpy.core.utils as utils
from dnfpy.model.mapDNF import MapDNF
from dnfpy.core.funcWithoutKeywords import FuncWithoutKeywords


class ModelWMCam(Model,Renderable):



    def initMaps(self,size):
        model = 'spike'
	self.size = size
        dt = 0.6
        wrap = True
	model_ = 'spike'
        #Input
        self.webcam = WebcamMap("Webcam",size,dt=dt,numDevice=0)
        self.color_select = ImageColorSelection("Color Select",size,dt=dt,thresh=5)

        mapSize = 0.3
        #Excitatory Memory
        self.fieldE = MapDNF("ExcitatoryField",size,dt=dt,mapSize=mapSize,model='spike',
                             iExc=2.2,iInh=1.5,
                             wExc=0.1/2.,wInh=0.2/2.)
        #Inhibition memory
        self.fieldI = MapDNF("InhibitoryField",size,dt=dt,mapSize=mapSize,model='spike',
                             iExc=2.2,iInh=1.5,
                             wExc=0.1/2.,wInh=0.2/2.,
                             h=-0.6)
        #artificial gaussian to bost inhbitory
        center = (size-1)/2
        self.gauss = FuncMap2D(utils.gauss2d,"ArtificialOnClickGaussian",
                               size=size,dt=dt,wrap=wrap,
                        intensity=0.,width=0.1*size,centerX=center,centerY=center)
        #TODO add unlimited amount of input to field
        self.add_gauss_and_input = FuncWithoutKeywords(utils.sumArrays,
                    "InputAndArtificialGaussian",size=size,dt=dt)
        self.add_gauss_and_input.addChildren(gauss=self.gauss,input=self.color_select)




        #Exc - Inh
        self.substract = FuncMap2D(utils.subArrays,"Exc - Inh",size,dt=0.1)

        #Neural field selection
        self.field = MapDNF("DNF",size,model='spike')

        #Link maps

        self.color_select.addChildren(image=self.webcam)
        self.aff = self.color_select

        #Excitatory
        self.fieldE.addChildren(aff=self.aff)

        #Inhibitory
        self.fieldI.addChildren(aff=self.add_gauss_and_input)

        #Exc - Inh
        self.substract.addChildren(a = self.fieldE.getActivation(),
                                   b = self.fieldI.getActivation())
        #Neural field

        self.field.addChildren(aff=self.substract)

        #return the root
        return self.field

    def getArrays(self):
        ret =  [
                        self.webcam,
                        self.aff,
                        self.substract,
                        self.gauss,
                        self.add_gauss_and_input,
                        self.fieldI.getActivation(),
                        self.fieldE.getActivation(),
                        self.field.getActivation(),
        ]
        return ret

    def onClick(self,mapName,x,y):
        print mapName.__class__
        if mapName == "Webcam":
            bgr = self.webcam.getData()
            
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
            return "Color Select"
	if mapName == "ArtificialOnClickGaussian":
       	    self.gauss.setParams(centerX=x,centerY=y,intensity=1.)



