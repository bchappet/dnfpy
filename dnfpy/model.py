import numpy as np
import sys
from funcMap2D import FuncMap2D
from inputMap import InputMap
from fieldMap import FieldMap
from activationMap import ActivationMap
from lateralWeightsMap import LateralWeightsMap



class Model(object):
    def __init__(self,globalParams):
        self.globalParams = globalParams
        self.initMaps()
#TODO transform into real params
        


    def initMaps(self):
        """We initiate the map and link them"""
        #Create maps
        size = self.globalParams['size']
        dt = self.globalParams['dt']
        self.aff = InputMap(size,self.globalParams['input_dt'],self.globalParams)
        self.field = FieldMap(size,dt,self.globalParams)
        self.activation = ActivationMap(size,dt,self.globalParams)
        self.lat = LateralWeightsMap(size,dt,self.globalParams)
        #Link maps
        self.field.addChildren({'afferent':self.aff,'lateral':self.lat})
        self.activation.addChildren({'field':self.field})
        self.lat.addChildren({'activation':self.activation})

    def run(self,timeEnd):
        simuTime = 0
        self.lat
        while simuTime < timeEnd:
            nextTime = self.field.getSmallestNextUpdateTime()
            simuTime = nextTime
            self.field.update(simuTime)
        
if __name__ == "__main__":
    args = sys.argv[1]
    params = eval(open(sys.argv[1],'r').read())
    model = Model(params)
    model.run(10)


        

