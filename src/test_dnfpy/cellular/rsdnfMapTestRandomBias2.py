import matplotlib.pyplot as plt
from dnfpy.core.constantMap import ConstantMap
import unittest
import numpy as np
from rsdnfMap import RsdnfMap
import dnfpy.view.staticViewMatplotlib as view

class RsdnfMapTestRandomBias(unittest.TestCase):
        def setUp(self):
                self.size = 101
                self.activation = np.zeros((self.size,self.size),np.bool_)
                self.uut = RsdnfMap("uut",self.size,routerType="sequenceShortMixte",activation=self.activation)
                self.uut.reset()


        def testComputeActivationNspike1(self):
            nspike = 1000
            self.uut.setParams(nspike=nspike,proba=0.99)
            self.activation[self.size//2,self.size//2] = 1
            for i in range(nspike*2):
                self.uut.compute()
            data = self.uut.getData()
            view.plotArray(data)
            view.show()


            plt.plot(data[self.size//2,:])
            plt.plot(data[:,self.size//2])
            plt.show()




               




if __name__ == "__main__":
        unittest.main()
