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


class ModelWMCam(Model,Renderable):



    def initMaps(self):
        """We initiate the map and link them"""
        #Input
        size = self.globalParams['size']
        self.webcam = WebcamMap(size)
        self.color_select = ImageColorSelection(size)

        #Memory
        self.fieldM = FieldMap(size)
        self.activationM = ActivationMap(size)
        sizeKM = size*0.3
        sizeKM = int(((sizeKM/2) * 2) + 1)#Ensure odd
        self.kernelM =  LateralWeightsMap(sizeKM,self.globalParams['lateralWKernel'],'KM')
        self.latM = Convolution(size)

        #Inhibition memory
        self.fieldI = FieldMap(size)
        self.activationI = ActivationMap(size)
        self.kernelI =  LateralWeightsMap(sizeKM,self.globalParams['lateralWKernel'],'KI')
        self.latI = Convolution(size)

        #Exc - Inh
        self.substract = FuncMap2D(utils.subArrays,size)

        #Neural field selection
        self.field = FieldMap(size)
        self.activation = ActivationMap(size)
        self.kernel =  LateralWeightsMap(size,self.globalParams['lateralWKernel'])
        self.lat = Convolution(size)

        #Link maps

        self.webcam.registerOnGlobalParamsChange(dt='webcam_dt')
        self.color_select.registerOnGlobalParamsChange(dt='webcam_dt',color='color',reverseColors='reverseColors',color_threshold='color_threshold')
        self.color_select.addChildren(image=self.webcam)
        self.aff = self.color_select


        #Memory
        self.fieldM.registerOnGlobalParamsChange(model='model',dt='dt',tau='tauM',h='hM',th='threshold')
        self.fieldM.addChildren(aff=self.aff,lat=self.latM)
        self.activationM.registerOnGlobalParamsChange(dt='dt',model='model',th='threshold')
        self.activationM.addChildren(field=self.fieldM)
        self.kernelM.registerOnGlobalParamsChange(dt='kernel_dt',wrap='wrap')
        self.latM.registerOnGlobalParamsChange(dt='dt',wrap='wrap')
        self.latM.addChildren(source=self.activationM,kernel = self.kernelM)

        #Inhibitory
        self.fieldI.registerOnGlobalParamsChange(model='model',dt='dt',tau='tauI',h='hM',th='threshold')
        self.fieldI.addChildren(aff=self.aff,lat=self.latI)
        self.activationI.registerOnGlobalParamsChange(dt='dt',model='model',th='threshold')
        self.activationI.addChildren(field=self.fieldI)
        self.kernelI.registerOnGlobalParamsChange(dt='kernel_dt',wrap='wrap')
        self.latI.registerOnGlobalParamsChange(dt='dt',wrap='wrap')
        self.latI.addChildren(source=self.activationI,kernel = self.kernelI)

        #Exc - Inh
        self.substract.registerOnGlobalParamsChange(dt='dt')
        self.substract.addChildren(a = self.activationM,b = self.activationI)



        #Neural field

        self.field.registerOnGlobalParamsChange(model='model',dt='dt',tau='tau',h='h',th='threshold')
        self.field.addChildren(aff=self.substract,lat=self.lat)
        self.activation.registerOnGlobalParamsChange(dt='dt',model='model',th='threshold')
        self.activation.addChildren(field=self.field)
        self.kernel.registerOnGlobalParamsChange(dt='kernel_dt',wrap='wrap')
        self.lat.registerOnGlobalParamsChange(dt='dt',wrap='wrap')
        self.lat.addChildren(source=self.activation,kernel = self.kernel)

        #Update args
        self.field.updateParams(self.globalParams)

        #Compute kernel once and for all
        self.kernelM.artificialRecursiveComputation()
        self.kernelI.artificialRecursiveComputation()
        self.kernel.artificialRecursiveComputation()

        #return the root
        return self.field

    def getArraysDict(self):
        return dict(
                        webcam = self.webcam.getData(),
                        colorSelect=self.aff.getData(),
                        #Working memory layer
                        WorkingMemory=self.fieldM.getData(),
                        WorkingMemoryLat=self.latM.getData(),
                        WorkingMemoryAct=self.activationM.getData(),
                        WorkingMemoryKernel = self.kernelM.getData(),
                        #Inhibition layer
                        InhibitoryMemory=self.fieldI.getData(),
                        InhibitoryLat=self.latI.getData(),
                        InhibitoryAct=self.activationI.getData(),
                        InhibitoryKernel = self.kernelI.getData(),
                        #Substarct
                        WM_Inh=self.substract.getData(),
                        #DNF layer
                        field=self.field.getData(),
                        lat=self.lat.getData(),
                        act=self.activation.getData(),
                        kernel = self.kernel.getData(),
                        )

