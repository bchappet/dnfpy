import unittest
import numpy as np
import matplotlib.pyplot as plt
import graphix
from dnfpy.model.lateralWeightsMap import *
import dnfpy.core.utils as utils

def constantArray(shape,value):
        arr =  np.zeros(shape)
        size = shape[0]
        center = (size-1)/2
        arr[center,center] = 1.
        return arr

class TestLateralWeightsMap(unittest.TestCase):
        def setUp(self):
                self.precision = 7
                self.size = 21
                self.uut = LateralWeightsMap(self.size,kernelType='gauss')
                self.uut.registerOnGlobalParamsChange(dt='dt',wrap='wrap')
                act = FuncMap2D(constantArray,self.size,value=1.,shape=((self.size,)*2))
                act.registerOnGlobalParamsChange(dt='dt')
                self.uut.addChildren(act=act)
                

                globalParams = dict(size=self.size,wrap=True,iExc=1.25,wExc=0.1,iInh=0.7,wInh=10.0,alpha=10.0,pExc =0.0043,pInh=0.5,dt=0.1 )
                self.uut.updateParams(globalParams)


        def test_gausiankernel(self):
                self.uut.update(0.1)
                expected =[-0.25281909, -0.25303704, -0.25323221, -0.25340453, -0.25355393, -0.2536751, \
                             -0.25346395, -0.24620937, -0.18000329,  0.03420243,  0.19954646,  0.03420243,\
                             -0.18000329, -0.24620937, -0.25346395, -0.2536751,  -0.25355393, -0.25340453,\
                             -0.25323221, -0.25303704, -0.25281909] 
                obtained =np.diagonal( self.uut.last_computation_args['kernel'])
                self.assertAlmostEqual(np.sum(expected-obtained),0,self.precision)
                #graphix.plotArray(self.uut.last_computation_args['kernel'])
                #plt.show()

        def test_convolution(self):
                self.uut.update(0.1)
                expected =[-0.25281909, -0.25303704, -0.25323221, -0.25340453, -0.25355393, -0.2536751, \
                             -0.25346395, -0.24620937, -0.18000329,  0.03420243,  0.19954646,  0.03420243,\
                             -0.18000329, -0.24620937, -0.25346395, -0.2536751,  -0.25355393, -0.25340453,\
                             -0.25323221, -0.25303704, -0.25281909] 
                obtained =np.diagonal( self.uut.getData())
                #graphix.plotArray(self.uut.getData())
                #plt.show()
                self.assertAlmostEqual(np.sum(expected-obtained),0,self.precision)





if __name__ == '__main__':
        unittest.main()




        

