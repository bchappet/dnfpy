import numpy as np
import utils
from funcWithoutKeywords import FuncWithoutKeywords
import unittest
from funcMap2D import FuncMap2D


class TestFuncWithoutKewords(unittest.TestCase):
    
    def setUp(self):
        self.precision = 7
        self.uut = FuncWithoutKeywords(1,0.1,{},utils.sumArrays)
        self.uut2 = FuncMap2D(1,0.1,{},utils.cosTraj, {'time':0.,'center':0.2,'radius':0.1,'period':10,'phase':0.2})
        self.uut.addChildren({'anything':self.uut2})


    def test_withChildren(self):
        """Methode compute
        scenario: we use a numpy function"""

        self.uut2.compute()
        self.uut.compute()
        expected = 0.23090169943749475
        obtained = self.uut.getData()
        self.assertAlmostEqual(expected,obtained,self.precision,"the result should be the same")

    def test_withConstant(self):
        self.uut = FuncWithoutKeywords(1,0.1,{},utils.sumArrays,[1,4,8])
        self.uut.compute()
        expected = 13
        obtained = self.uut.getData()
        self.assertEqual(expected,obtained,"the result should be the same")

    def test_withBoth(self):
        self.uut = FuncWithoutKeywords(1,0.1,{},utils.sumArrays,[1,4,8])
        self.uut.addChildren({'uut2':self.uut2})
        self.uut2.compute()
        self.uut.compute()
        expected = 13 + 0.23090169943749475
        obtained = self.uut.getData()
        self.assertAlmostEqual(expected,obtained,self.precision,"the result should be the same")
    def test_sumArray(self):
        self.uut = FuncWithoutKeywords(1,0.1,{},utils.sumArrays,[[1,2],[3,4],[4,5]])
        self.uut.compute()
        expected = [8,11]
        obtained = self.uut.getData()
        self.assertTrue((expected==obtained).all(),"The result should be the same")



        



if __name__ == '__main__':
    unittest.main()



