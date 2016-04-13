from dnfpy.core.constantMap import ConstantMap
import unittest
import numpy as np
from rsdnfMap import RsdnfMap
import dnfpy.view.staticViewMatplotlib as view
import matplotlib.pyplot as plt

class RsdnfMapTestError(unittest.TestCase):
        def setUp(self):
                self.size = 10
                self.activation = np.zeros((self.size,self.size),np.intc)
                self.uut = RsdnfMap("uut",self.size,activation=self.activation)
                self.uut.reset()

        
        def testComputeP1(self):
            self.uut.setParams(errorType='transient')
            self.activation[self.size//2,self.size//2] = 1
        
            for i in range(10):
                self.uut.compute()
                data = self.uut.getData()
                print(data)
            self.assertEqual(data[self.size//2+1,self.size//2+1],20)


if __name__ == "__main__":
        unittest.main()
