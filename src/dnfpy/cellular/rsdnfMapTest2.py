
from dnfpy.core.constantMap import ConstantMap
import unittest
import numpy as np
from rsdnfMap import RsdnfMap
import dnfpy.view.staticViewMatplotlib as view

class RsdnfMapTestSequence(unittest.TestCase):
        def setUp(self):
                self.size = 51
                self.activation = np.zeros((self.size,self.size),np.bool_)
                
                self.uut = RsdnfMap("uut",self.size,routerType="sequence",activation=self.activation)
                
        def testComputeP(self):
            self.activation[self.size//2,self.size//2] = True
            for i in range(100):
                self.uut.compute()
            data = self.uut.getData()

        def testComputeP1(self):
            self.activation[self.size//2,self.size//2] = True
            self.uut.setParams(proba=0.99)

            for i in range(50):
                self.uut.compute()
                randomSequence = self.uut.getRandomSequence()
                #print(randomSequence[:,:,2])
            data = self.uut.getData()
            view.plotArray(data)
            view.show()

                

                




if __name__ == "__main__":
        unittest.main()
