
from dnfpy.core.constantMap import ConstantMap
import unittest
import numpy as np
from rsdnfMap import RsdnfMap
import dnfpy.view.staticViewMatplotlib as view

class RsdnfMap_est(unittest.TestCase):
        def setUp(self):
                self.size = 100
                self.activation = np.zeros((self.size,self.size),np.bool_)
                self.uut = RsdnfMap("uut",self.size,activation=self.activation)

        def testConstruct(self):
                print(self.uut.getData())
        
        def testComputeP1(self):
            self.activation[self.size/2,self.size/2] = 1
        
            for i in range(100):
                self.uut.compute()
                data = self.uut.getData()

        def testComputeP2(self):
            self.activation[self.size/2,self.size/2] = 1
            self.uut.setParams(proba=0.99)
            for i in range(100):
                self.uut.compute()
            data = self.uut.getData()


        def tes_ComputePrecision(self):#TODO
            self.activation[self.size/2,self.size/2] = 1
            self.uut.setParams(proba=0.99)
            self.uut.setParams(precision=1)
            for i in range(100):
                self.uut.compute()
            data = self.uut.getData()
            view.plotArray(data)
            view.show()

class RsdnfMapTestSequence(unittest.TestCase):
        def setUp(self):
                self.size = 100
                self.activation = np.zeros((self.size,self.size),np.bool_)
                self.uut = RsdnfMap("uut",self.size,routerType="sequence",activation=self.activation)
                
        def testComputeP(self):
            self.activation[self.size/2,self.size/2] = 1
            for i in range(100):
                print("i ",i)
                self.uut.compute()
            data = self.uut.getData()
            view.plotArray(data)
            view.show()

                




if __name__ == "__main__":
        unittest.main()
