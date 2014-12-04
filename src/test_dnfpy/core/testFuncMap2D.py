import unittest
from dnfpy.core.funcMap2D import FuncMap2D
import dnfpy.core.utils as utils
import numpy as np
import os

class TestFuncMap2D(unittest.TestCase):
    def setUp(self):
        path =  os.path.dirname(os.path.realpath(__file__))
        self.testDir =path +  "/testFiles/"
        self.precision = 7

        self.size = 10
        self.dt = 0.1
        self.func = utils.gauss2d

        self.uut = FuncMap2D(self.func,self.size,dt=self.dt,wrap=True,
                             intensity=10,width=4,centerX=7,centerY=1)

        func2 = utils.cosTraj
        self.uut2 = FuncMap2D(func2,1,dt=0.1,center=0.2,
                              radius=0.1,period=10,phase=0.2)

    def test_computeGauss2d(self):
        """Method: compute
        scenario: the func is gauss2d and the args are 10,wrap,10,4,7,1"""
        self.uut.update(0.1)
        expected1 = np.loadtxt(self.testDir+"testGauss2DWrap.csv",dtype=np.float32,delimiter=",")
        obtained1 = self.uut.getData()
        self.assertTrue((expected1==obtained1).all(),"the result should be the same")

    def test_changeParams(self):
        """Method updateParams
        scenario: we update the params"""
        self.uut.setArg(wrap=False)
        self.uut.update(0.1)
        expected = np.loadtxt(self.testDir+"testGauss2DWrap.csv",dtype=np.float32,delimiter=",")
        obtained = self.uut.getData()
        self.assertFalse((expected==obtained).all(),"we changed the params, the results should be different")

    def test_funcWithAttributeParamsT01(self):
        """Method mapAttributesToFunc
        scenario : we map the time to utils.cosTraj func
        we compute with update"""
        self.uut2.update(0.1)
        obtained = self.uut2.getData()
        expected = 0.23681245526846784
        self.assertAlmostEqual(expected,obtained,self.precision,"the result should be the same")
    def test_funcWithAttributeParamsT1(self):
        """Method mapAttributesToFunc
        scenario : we map the time to utils.cosTraj func
        we compute with update until 1 sec"""
        for time in np.arange(0.1,1.1,0.1):
            self.uut2.update(time)

        obtained = self.uut2.getData()
        expected = 0.28090169943749477
        self.assertAlmostEqual(expected,obtained,self.precision,"the result should be the same")




    def test_addChildren(self):
        """Method addChildren
        scenario:we add one children and we update"""
        self.uut.addChildren(centerX=self.uut2)
        self.uut.update(0.1)
        expected = 0.23681245526846784
        obtained = self.uut2.getData()
        self.assertAlmostEqual(expected,obtained,self.precision,"The computation of the child should be as expected")

        #expected = 7.3161559
        expected = 2.5362177
        obtained = self.uut.getData()[3,6]
        self.assertAlmostEqual(expected,obtained,self.precision,"The computation of uut should take the child as parameter for centerX")

    def test_constantArgs(self):
        """Test with only constant args"""
        func2 = utils.cosTraj
        self.uut2 = FuncMap2D(func2,1,dt=0.1,time=0.1,center=0.2,radius=0.1,period=10,phase=0.2)
        self.uut2.update(0.1)
        expected = 0.23681245526846784
        obtained = self.uut2.getData()
        self.assertAlmostEqual(expected,obtained,self.precision,"The computation of  should be as expected")

    def test_constantArgs_attribute_andGlobalArgs(self):
        func2 = utils.cosTraj
        self.uut2 = FuncMap2D(func2,1,dt=0.1,radius=0.1,period=10,phase=0.2,center=0.2)

        self.uut2.update(0.1)

        expected = 0.23681245526846784
        obtained = self.uut2.getData()
        self.assertAlmostEqual(expected,obtained,self.precision,"The computation of  should be as expected")

    def test_constantArgs_attribute_andGlobalArgs_changeArgs(self):
        """Scenario : change args after 1 computation"""
        func2 = utils.cosTraj
        self.uut2 = FuncMap2D(func2,1,dt=0.1,radius=0.1,period=10,phase=0.2,center=0.2)
        self.uut2.update(0.1)
        self.uut2.setArg(center=0.3)
        self.uut2.update(0.2)
        expected = 0.34257792915650725
        obtained = self.uut2.getData()
        self.assertAlmostEqual(expected,obtained)

if __name__ == '__main__':
    unittest.main()


