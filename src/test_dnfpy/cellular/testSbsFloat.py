import time

import numpy as np
import matplotlib.pyplot as plt
from dnfpy.cellular.sbsFloatMap import SbsFloatMap
from dnfpy.core.constantMap import ConstantMap
import dnfpy.view.staticViewMatplotlib as view

import unittest

class TestSbsFloatMap(unittest.TestCase):
    def setUp(self):
        self.size = 49
        self.activation = np.zeros((self.size,self.size),np.intc)
        activationMap = ConstantMap("actmap",self.size, self.activation)
        self.uut = SbsFloatMap("uut",self.size)
        self.uut.addChildren(activation=activationMap)


    def testSetGetVslue(self):
        value = np.random.random((self.size,self.size)).astype(np.float32)
        value1 = np.zeros((self.size,self.size),dtype=np.float32)
        self.uut.lib.setArrayAttribute(SbsFloatMap.Attributes.VALUE,value)
        self.uut.lib.getArrayAttribute(SbsFloatMap.Attributes.VALUE,value1)

        self.assertTrue(np.all(value == value1))



    def test_update(self):
        self.uut.compute()
        data = self.uut.getData()
        self.assertEqual(np.sum(data),0)

    def test_update_act(self):
        self.uut.setParams(probaSpike=1.0,probaSynapse=0.9)
        data = self.getData()
        print("min : %s, max: %s, sum: %s"%(np.min(data),np.max(data),np.sum(data)))
        view.plotArray(data)
        view.show()

    def getData(self):
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                self.activation[self.size//2+i][self.size//2+j] = 1;
        start = time.clock()
        self.uut.compute()
        end = time.clock()
        print("elapsed time %s"%(end-start))
        data = self.uut.getData()
        return data

  

if __name__ == "__main__":
    unittest.main()





