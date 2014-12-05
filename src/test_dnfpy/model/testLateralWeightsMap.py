import unittest
import numpy as np
from dnfpy.model.convolution import Convolution
from dnfpy.model.lateralWeightsMap import LateralWeightsMap
from dnfpy.core.funcMap2D import FuncMap2D

def constantArray(shape,value):
        arr =  np.zeros(shape)
        size = shape[0]
        center = (size-1)/2
        arr[center,center] = 1.
        return arr

class TestLateralWeightsMapAndConvolution(unittest.TestCase):
        def setUp(self):
                self.precision = 7
                self.size = 21
                self.kernel = LateralWeightsMap( \
                    21,1, 10e8, True, 1.25, 0.7, 0.1, 10.0, alpha=10)
                act = FuncMap2D(constantArray,self.size,dt=0.1,value=1.,
                                shape=((self.size,)*2))
                self.uut = Convolution(self.size,dt=0.1,wrap=True)
                self.uut.addChildren(source=act,kernel=self.kernel)
                self.kernel.compute()



        def test_gausiankernel(self):
                self.uut.update(0.1)
                expected =[-0.25281909, -0.25303704, -0.25323221, -0.25340453, -0.25355393, -0.2536751, \
                             -0.25346395, -0.24620937, -0.18000329,  0.03420243,  0.19954646,  0.03420243,\
                             -0.18000329, -0.24620937, -0.25346395, -0.2536751,  -0.25355393, -0.25340453,\
                             -0.25323221, -0.25303704, -0.25281909]
                obtained =np.diagonal( self.kernel.getData())
                self.assertAlmostEqual(np.sum(expected-obtained),0,self.precision)

        def test_convolution(self):
                self.uut.update(0.1)
                expected =[-0.25281909, -0.25303704, -0.25323221, -0.25340453, -0.25355393, -0.2536751, \
                             -0.25346395, -0.24620937, -0.18000329,  0.03420243,  0.19954646,  0.03420243,\
                             -0.18000329, -0.24620937, -0.25346395, -0.2536751,  -0.25355393, -0.25340453,\
                             -0.25323221, -0.25303704, -0.25281909]
                obtained =np.diagonal( self.uut.getData())
                self.assertAlmostEqual(np.sum(expected-obtained),0,self.precision)
        def test_gausiankernel_smaller(self):
                self.kernel = LateralWeightsMap( \
                    21,0.5, 10e8, True, 1.25, 0.7, 0.1, 10.0, alpha=10)
                self.kernel.compute()
                obtained =np.diagonal( self.kernel.getData())
                self.assertEqual(len(obtained),11)

        def test_gausiankernel_smaller_ensure_odd(self):
                self.kernel = LateralWeightsMap( \
                    21,0.3, 10e8, True, 1.25, 0.7, 0.1, 10.0, alpha=10)
                self.kernel.compute()
                obtained =np.diagonal( self.kernel.getData())
                self.assertEqual(len(obtained),7)
        def test_gausiankernel_ensure_odd(self):
                self.kernel = LateralWeightsMap( \
                    21,1., 10e8, True, 1.25, 0.7, 0.1, 10.0, alpha=10)
                self.kernel.compute()
                obtained =np.diagonal( self.kernel.getData())
                self.assertEqual(len(obtained),21)

if __name__ == '__main__':
        unittest.main()
