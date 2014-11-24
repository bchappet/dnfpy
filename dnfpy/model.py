import numpy as np
import sys
from funcMap2D import FuncMap2D
from inputMap import InputMap
from fieldMap import FieldMap
from activationMap import ActivationMap
from lateralWeightsMap import LateralWeightsMap
import matplotlib.pyplot as plt



class Model(object):
    def __init__(self,globalParams):
        self.globalParams = globalParams
        self.initMaps()

    def initMaps(self):
        """We initiate the map and link them"""
        #Create maps
        size = self.globalParams['size']
        self.aff = InputMap(size)
        self.field = FieldMap(size)
        self.activation = ActivationMap(size)
        self.lat = LateralWeightsMap(size,self.globalParams['lateralWKernel'])
        #Link maps
        self.aff.registerOnGlobalParamsChange_ignoreCompute(dt='input_dt',nb_distr='nbDistr')


        self.field.registerOnGlobalParamsChange(model='model',dt='dt',tau='tau',h='h',th='threshold')
        self.field.addChildren(aff=self.aff,lat=self.lat)

        self.activation.registerOnGlobalParamsChange(dt='dt',model='model',th='threshold')
        self.activation.addChildren(field=self.field)

        self.lat.registerOnGlobalParamsChange(wrap='wrap')
        self.lat.addChildren(activation=self.activation)

        #Update args
        self.field.updateParams(self.globalParams)

    def run(self,timeEnd):
        simuTime = 0
        self.lat
        while simuTime < timeEnd:
            nextTime = self.field.getSmallestNextUpdateTime()
            simuTime = nextTime
            self.field.update(simuTime)

        plt.imshow(self.field.getData())
        plt.show()
        
if __name__ == "__main__":
    args = sys.argv[1]
    params = eval(open(sys.argv[1],'r').read())
    model = Model(params)
    model.run(10)


        

