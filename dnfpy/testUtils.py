from utils import *
import unittest
import numpy as np


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.dir = "./testFiles/"
    def test_gauss2DWrap(self):
        """Function : gaus2D
        Scenario : wrap"""
        expected1 = np.loadtxt(self.dir+"testGauss2DWrap.csv",dtype=np.float32,delimiter=",")
        obtained1 = gauss2d(10,True,10,4,[7,1])

        self.assertTrue((expected1==obtained1).all(),"the result should be the same")

    def test_gauss2DNoWrap(self):
        """Function : gaus2D
        Scenario : no wrap"""
        expected = np.loadtxt(self.dir+"testGauss2DNoWrap.csv",dtype=np.float32,delimiter=",")
        obtained = gauss2d(10,False,10,4,[7,1])
        self.assertTrue((expected==obtained).all(),"the result should be the same")

    def test_exp2DWrap(self):
        """Function : exp2D
        Scenario : wrap"""
        expected = np.loadtxt(self.dir+"testExp2DWrap.csv",dtype=np.float32,delimiter=",")
        obtained = exp2d(10,True,10,4,[7,1])
        self.assertTrue((expected==obtained).all(),"the result should be the same")

    def test_exp2DNoWrap(self):
        """Function : exp2D
        Scenario : no wrap"""
        expected = np.loadtxt(self.dir+"testExp2DNoWrap.csv",dtype=np.float32,delimiter=",")
        obtained = exp2d(10,False,10,4,[7,1])
        self.assertTrue((expected==obtained).all(),"the result should be the same")



if __name__ == '__main__':
    unittest.main()





