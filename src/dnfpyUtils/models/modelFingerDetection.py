from dnfpy.core.funcMap2D import FuncMap2D
from dnfpy.core.funcWithoutKeywords import FuncWithoutKeywords
import dnfpy.core.utils as utils
from dnfpy.model.inputMap import InputMap
from dnfpy.model.fieldMap import FieldMap
from dnfpy.model.activationMap import ActivationMap
from dnfpy.model.lateralWeightsMap import LateralWeightsMap
from dnfpy.model.webcamMap import WebcamMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.imageColorSelection import ImageColorSelection
from dnfpy.model.onOffFilter import OnOffFilter
from dnfpy.model.convolution import Convolution
import cv2


class ModelFingerDetection(Model,Renderable):

    def initMaps(self):
        """We initiate the map and link them"""
        #Create maps
        size = self.globalParams['size']

        self.webcam = WebcamMap(size)
        self.color_select = ImageColorSelection(size)
        self.onOff1 = OnOffFilter(size=60,
                    onIntXY=(1,1),onStdXY = (0.1,0.5),
                    offIntXY = (0.7,0.7), offStdXY = (0.1,0.5), 
                    shift = 0.2)
        self.onOff2 = OnOffFilter(size=20,
                    onIntXY=(1,1),onStdXY = (0.1,0.5),
                    offIntXY = (0.7,0.7), offStdXY = (0.1,0.5), 
                    shift = 0.2)

        self.convo1 = Convolution(size)
        self.convo2 = Convolution(size)
        self.aff = FuncWithoutKeywords(utils.sumArrays,size)

        #Link maps
        self.webcam.registerOnGlobalParamsChange(dt='dt') 

        self.color_select.registerOnGlobalParamsChange(dt='dt',color='color',reverseColors='reverseColors',color_threshold='color_threshold')
        self.color_select.addChildren(image=self.webcam)

        self.onOff1.registerOnGlobalParamsChange(dt='kernel_dt')
        self.onOff2.registerOnGlobalParamsChange(dt='kernel_dt')

        self.convo1.registerOnGlobalParamsChange(dt='dt',wrap='wrap')
        self.convo2.registerOnGlobalParamsChange(dt='dt',wrap='wrap')
        self.convo1.addChildren(source=self.color_select,kernel = self.onOff1)
        self.convo2.addChildren(source=self.color_select,kernel = self.onOff2)
        

        self.aff.registerOnGlobalParamsChange_ignoreCompute(dt='dt')
        self.aff.addChildren(
                        color=self.color_select,
                        convo1=self.convo1,
                        convo2=self.convo2,
                        )


        #Update args
        self.aff.updateParams(self.globalParams)

        #Compute onOff once and for all
        self.onOff1.artificialRecursiveComputation()
        self.onOff2.artificialRecursiveComputation()

        #return the root
        return self.aff

    def getArraysDict(self):
        return dict(
                        webcam = self.webcam.getData(),
                        aff=self.aff.getData(),
                        onOff1 = self.onOff1.getData(),
                        onOff2 = self.onOff2.getData(),
                        convo1 = self.convo1.getData(),
                        convo2 = self.convo2.getData(),
                        color=self.color_select.getData()
                    )

