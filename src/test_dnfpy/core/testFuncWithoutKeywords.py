import numpy as np
import unittest
from dnfpy.core.funcWithoutKeywords import FuncWithoutKeywords
from dnfpy.core.funcMap2D import FuncMap2D
import dnfpy.core.utils as utils


class TestFuncWithoutKewords(unittest.TestCase):
    
    def setUp(self):
        self.precision = 7
        self.uut = FuncWithoutKeywords(utils.sumArrays,1,dt=0.1)
        self.uut.ignoreComputeArgs('dt')
        self.uut2 = FuncMap2D(utils.cosTraj,1,dt=0.1,**{'time':0.,'center':0.2,'radius':0.1,'period':10,'phase':0.2})
        self.uut.addChildren(**{'child':self.uut2})


    def test_withChildren(self):
        """Methode compute
        scenario: we use a numpy function"""

        self.uut2.update(0.1)
        self.uut.update(0.1)
        expected = 0.236812455268
        obtained = self.uut.getData()
        self.assertAlmostEqual(expected,obtained,self.precision,"the result should be the same")

    def test_withConstant(self):
        self.uut = FuncWithoutKeywords(utils.sumArrays,1,dt=0.1,a=1,b=4,c=8)
        self.uut.ignoreComputeArgs('dt')
        self.uut.update(0.1)
        expected = 13
        obtained = self.uut.getData()
        self.assertEqual(expected,obtained,"the result should be the same")

    def test_withBoth(self):
        self.uut = FuncWithoutKeywords(utils.sumArrays,1,dt=0.1,a=1,b=4,c=8)
        self.uut.ignoreComputeArgs('dt')
        self.uut.addChildren(uut2=self.uut2)
        self.uut2.update(0.1)
        self.uut.update(0.1)
        expected = 13 + 0.236812455268
        obtained = self.uut.getData()
        self.assertAlmostEqual(expected,obtained,self.precision,"the result should be the same")
    def test_sumArray(self):
        self.uut = FuncWithoutKeywords(utils.sumArrays,1,dt=0.1,a=[1,2],b=[3,4],c=[4,5])
        self.uut.ignoreComputeArgs('dt')
        self.uut.update(0.1)
        expected = [8,11]
        obtained = self.uut.getData()
        self.assertTrue((expected==obtained).all(),"The result should be the same")
    def test_register_on_param_change_igore(self):
        self.uut = FuncWithoutKeywords(utils.sumArrays,1,a=[1,2],b=[3,4],c=[4,5])
        self.uut.registerOnGlobalParamsChange_ignoreCompute(dt='dt')
        self.uut.updateParams({'dt':0.1})
        self.uut.update(0.1)
        expected = [8,11]
        obtained = self.uut.getData()
        self.assertTrue((expected==obtained).all(),"The result should be the same")




        



if __name__ == '__main__':
    unittest.main()



