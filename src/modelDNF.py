from dnfpy.core.funcMap2D import FuncMap2D
from dnfpy.model.inputMap import InputMap
from dnfpy.model.fieldMap import FieldMap
from dnfpy.model.activationMap import ActivationMap
from dnfpy.model.lateralWeightsMap import LateralWeightsMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.convolution import Convolution


class ModelDNF(Model,Renderable):
    def initMaps(self):
        """We initiate the map and link them"""
        #Create maps
        size = self.globalParams['size']
        self.aff = InputMap(size)
        self.field = FieldMap(size)
        self.activation = ActivationMap(size)
        self.kernel = LateralWeightsMap(size,self.globalParams['lateralWKernel'])
        self.lat = Convolution(size)
        #Link maps
        self.aff.registerOnGlobalParamsChange_ignoreCompute(dt='input_dt',nb_distr='nbDistr')


        self.field.registerOnGlobalParamsChange(model='model',dt='dt',tau='tau',h='h',th='threshold')
        self.field.addChildren(aff=self.aff,lat=self.lat)

        self.activation.registerOnGlobalParamsChange(dt='dt',model='model',th='threshold')
        self.activation.addChildren(field=self.field)

        self.kernel.registerOnGlobalParamsChange(dt = 'kernel_dt')
        self.lat.registerOnGlobalParamsChange(dt='dt',wrap='wrap')
        self.lat.addChildren(source=self.activation,kernel = self.kernel)

        #Update args
        self.field.updateParams(self.globalParams)
        #Update once and for all the kernel
        self.kernel.artificialRecursiveComputation()

        #return the root
        return self.field

    def getArraysDict(self):
        return dict(aff=self.aff.getData(),field=self.field.getData(),lat=self.lat.getData(),act=self.activation.getData())


