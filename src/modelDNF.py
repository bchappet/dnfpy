import numpy as np
import sys
from dnfpy.core.funcMap2D import FuncMap2D
from dnfpy.model.inputMap import InputMap
from dnfpy.model.fieldMap import FieldMap
from dnfpy.model.activationMap import ActivationMap
from dnfpy.model.lateralWeightsMap import LateralWeightsMap
import matplotlib.pyplot as plt
import test_dnfpy.model.graphix as graphix
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model


class ModelDNF(Model,Renderable):

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

        self.lat.registerOnGlobalParamsChange(dt='dt',wrap='wrap')
        self.lat.addChildren(act=self.activation)

        #Update args
        self.field.updateParams(self.globalParams)

        #return the root
        return self.field

    def getArraysDict(self):
        return dict(aff=self.aff.getData(),field=self.field.getData(),lat=self.lat.getData(),act=self.activation.getData())

    
def run(model,timeEnd):
    """Will be the controller"""
    simuTime = 0
    while simuTime < timeEnd:
        nextTime = model.getSmallestNextUpdateTime()
        simuTime = nextTime
        model.update(simuTime)
def plot(model):
    """Will be the view"""
    graphix.plotMaps(model.getMapsToDisplay())
    plt.show()
    

if __name__ == "__main__":
    args = sys.argv[1] #name of the file containing the global argument dictionary
    params = eval(open(sys.argv[1],'r').read()) #should separate args commandline, arg controler and arg view and arg model
    model = Model(params)
    run(model,params['time_end'])
    plot(model)




        

