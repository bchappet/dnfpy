from dnfpy.core.utils import *
import unittest
import numpy as np
import os


class TestUtils(unittest.TestCase):
    def setUp(self):
        path =  os.path.dirname(os.path.realpath(__file__))
        self.testDir =path +  "/testFiles/"
        self.precision = 7
    def test_gauss2DWrap(self):
        """Function : gaus2D
        Scenario : wrap"""
        expected1 = np.loadtxt(self.testDir+"testGauss2DWrap.csv",dtype=np.float32,delimiter=",")
        obtained1 = gauss2d(10,True,10,4,7,1)

        self.assertTrue((expected1==obtained1).all(),"the result should be the same")

    def test_gauss2DNoWrap(self):
        """Function : gaus2D
        Scenario : no wrap"""
        expected = np.loadtxt(self.testDir+"testGauss2DNoWrap.csv",dtype=np.float32,delimiter=",")
        obtained = gauss2d(10,False,10,4,7,1)
        self.assertTrue((expected==obtained).all(),"the result should be the same")

    def test_exp2DWrap(self):
        """Function : exp2D
        Scenario : wrap"""
        expected = np.loadtxt(self.testDir+"testExp2DWrap.csv",dtype=np.float32,delimiter=",")
        obtained = exp2d(10,True,10,4,7,1)
        self.assertTrue((expected==obtained).all(),"the result should be the same")

    def test_exp2DNoWrap(self):
        """Function : exp2D
        Scenario : no wrap"""
        expected = np.loadtxt(self.testDir+"testExp2DNoWrap.csv",dtype=np.float32,delimiter=",")
        obtained = exp2d(10,False,10,4,7,1)
        self.assertTrue((expected==obtained).all(),"the result should be the same")
        
    def test_cosTraj(self):
        """Function: cosTraj
        scenario standard"""
        expected = 0.13090169943749475
        obtained = cosTraj(0.1,0.1,0.1,0.1,0.2)
        self.assertAlmostEqual(expected,obtained,self.precision,"the result should be the same")
        expected = 2.0
        obtained = cosTraj(1,1,1,1,1)
        self.assertAlmostEqual(expected,obtained,self.precision,"the result should be the same")
    def test_sumArrays(self):
        """Function sumArray
        scenario sum 3 array"""
        a = [1,2]
        b = [2,3]
        c = [2,7]
        expected = [5,12]
        obtained=sumArrays(a,b,c)
        self.assertTrue((expected==obtained).all(),"the result should be the same")


if __name__ == '__main__':
    unittest.main()





