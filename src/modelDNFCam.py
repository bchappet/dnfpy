import numpy as np
import sys
from dnfpy.core.funcMap2D import FuncMap2D
from dnfpy.model.inputMap import InputMap
from dnfpy.model.fieldMap import FieldMap
from dnfpy.model.activationMap import ActivationMap
from dnfpy.model.lateralWeightsMap import LateralWeightsMap
from dnfpy.model.webcamMap import WebcamMap
import matplotlib.pyplot as plt
import test_dnfpy.model.graphix as graphix
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.imageColorSelection import ImageColorSelection


class ModelDNFCam(Model,Renderable):

    def initMaps(self):
        """We initiate the map and link them"""
        #Create maps
        size = self.globalParams['size']

        self.webcam = WebcamMap(size)
        self.color_select = ImageColorSelection(size)
        self.field = FieldMap(size)
        self.activation = ActivationMap(size)
        self.lat = LateralWeightsMap(size,self.globalParams['lateralWKernel'])
        #Link maps

        self.webcam.registerOnGlobalParamsChange(dt='webcam_dt') 
        self.color_select.registerOnGlobalParamsChange(dt='webcam_dt',color='color',reverseColors='reverseColors',color_threshold='color_threshold')
        self.color_select.addChildren(image=self.webcam)
        self.aff = self.color_select


        self.field.registerOnGlobalParamsChange(model='model',dt='dt',tau='tau',h='h',th='threshold')
        self.field.addChildren(aff=self.aff,lat=self.lat)

        self.activation.registerOnGlobalParamsChange(dt='dt',model='model',th='threshold')
        self.activation.addChildren(field=self.field)

        self.lat.registerOnGlobalParamsChange(dt='dt',wrap='wrap')
        self.lat.addChildren(act=self.activation)

        #Update args
        self.field.updateParams(self.globalParams)

        #return the root
        return self.field

    def getArraysDict(self):
        return dict(webcam = self.webcam.getData(),aff=self.aff.getData(),field=self.field.getData(),lat=self.lat.getData(),act=self.activation.getData())

