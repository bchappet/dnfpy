import unittest
from funcMap2D import FuncMap2D
import utils
import numpy as np

class TestFuncMap2D(unittest.TestCase):
    
    def setUp(self):
        self.dir = "./testFiles/"
        self.precision = 10

        self.size = 10
        self.dt = 1
        self.globalRealParams = {'size':10,'wrap':True,'iA':10,'wA':4,'cX':7,'cY':1}
        self.argNamesDict = {'size':'size','wrap':'wrap','intensity':'iA','width':'wA','centerX':'cX','centerY':'cY'}
        self.func = utils.gauss2d

        self.uut = FuncMap2D(self.size,self.dt,self.globalRealParams,self.func,self.argNamesDict)

        #Another one
        globalRealParams2 = {'c':0.2,'r':0.1,'p':10,'ph':0.2}
        argNamesDict2 = {'center':'c','radius':'r','period':'p','phase':'ph'}
        func2 = utils.cosTraj
        self.uut2 = FuncMap2D(1,0.1,globalRealParams2,func2,argNamesDict2)
        self.uut2.mapAttributesToFunc({'time':self.uut2.getTime})

    def test_computeGauss2d(self):
        """Method: compute
        scenario: the func is gauss2d and the args are 10,wrap,10,4,7,1"""
        self.uut.compute()
        expected1 = np.loadtxt(self.dir+"testGauss2DWrap.csv",dtype=np.float32,delimiter=",")
        obtained1 = self.uut.getData()
        self.assertTrue((expected1==obtained1).all(),"the result should be the same") 

    def test_changeParams(self):
        """Method updateParams
        scenario: we update the params"""
        self.globalRealParams['wrap'] = False
        self.uut.updateParams(self.globalRealParams)
        self.uut.compute()
        expected = np.loadtxt(self.dir+"testGauss2DWrap.csv",dtype=np.float32,delimiter=",")
        obtained = self.uut.getData()
        self.assertFalse((expected==obtained).all(),"we changed the params, the results should be different") 

    def test_funcWithAttributeParamsT0(self):
        """Method mapAttributesToFunc
        scenario : we map the time to utils.cosTraj func
        we compute without update"""
        self.uut2.compute()
        obtained = self.uut2.getData()
        expected = 0.23090169943749475
        self.assertAlmostEqual(expected,obtained,self.precision,"the result should be the same")
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
        scenario:we add one children and we compue"""
        #globalRealParams = {'time'
        #child = FuncMap2D(1,0.1,






if __name__ == '__main__':
    unittest.main()


