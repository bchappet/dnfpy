from dnfpy.core.constantMap import ConstantMap
import unittest
import numpy as np
from nSpikeMap import NSpikeMap
import dnfpy.view.staticViewMatplotlib as view

class NSpikeMapTest(unittest.TestCase):
        def setUp(self):
                self.size = 100
                self.activation = np.zeros((self.size,self.size),np.bool_)
                self.uut = NSpikeMap("uut",self.size,activation=self.activation)
                self.uut.reset()

        
        def testComputeP1(self):
            self.activation[self.size//2,self.size//2] = 1
        
            for i in range(100):
                self.uut.compute()
                data = self.uut.getData()
            self.assertEqual(data[self.size//2+1,self.size//2+1],20)

        def testComputationStart(self):
            self.activation[self.size//2,self.size//2] = 1
        
            self.uut.compute()
            data = self.uut.getData()
            view.plotArray(data)
            view.show()



if __name__ == "__main__":
        unittest.main()
