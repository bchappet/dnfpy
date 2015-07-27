import unittest
import numpy as np
from dnfpy.cellular.nSpikeMap import NSpikeMap

class TestNSpikeMap(unittest.TestCase):
    def setUp(self):
        self.size = 11
        self.activation = np.zeros((self.size,self.size),np.intc)
        self.uut = NSpikeMap("uut",self.size,activation=self.activation)

    def test_update(self):
        self.uut.compute()
        self.assertEqual(np.sum(self.uut.getData()),0)

    def test_activation(self):
        self.activation[2][5] = 1
        self.uut.compute()
        res = self.uut.getData()
        self.assertEquals(res[2][5],0)
        self.assertEquals(res[0][0],20)

    def test_2activation(self):
        self.activation[2][5] = 1
        self.activation[5][2] = 1
        self.uut.compute()
        res = self.uut.getData()
        self.assertEquals(res[2][5],20)
        self.assertEquals(res[0][0],40)

    def test_proba_0(self):
        self.uut.setParams(proba=0.)
        self.activation[2][5] = 1
        self.uut.compute()
        res = self.uut.getData()
        self.assertEquals(res[2][5],0)
        self.assertEquals(res[0][0],0)

    def test_activation_n10(self):
        self.uut.setParams(nspike=10)
        self.activation[2][5] = 1
        self.uut.compute()
        res = self.uut.getData()
        self.assertEquals(res[2][5],0)
        self.assertEquals(res[0][0],10)

    def test_proba_09(self):
        self.uut.setParams(proba=0.9)
        self.activation[5][5] = 1
        self.uut.compute()
        res = self.uut.getData()
        self.assertTrue(([7,9,10,10,10,11,10,8,6,5,5]==res[0]).all())

    def test_reset_reproductibilite(self):
        self.uut.setParams(proba=0.9)
        self.activation[5][5] = 1
        self.uut.compute()
        res1 = self.uut.getData()
        self.uut.reset()
        self.assertEqual(0.9,self.uut.getArg("proba"))
        self.activation[5][5] = 1
        self.uut.compute()
        res2 = self.uut.getData()
        self.assertTrue((res1==res2).all())

    def test_reset_non_reproductibilite(self):
        self.uut = NSpikeMap("uut",self.size,activation=self.activation,
                             reproductible=False)
        self.uut.setParams(proba=0.9)
        self.activation[5][5] = 1
        self.uut.compute()
        res1 = self.uut.getData()
        self.uut.reset()
        self.assertEqual(0.9,self.uut.getArg("proba"))
        self.activation[5][5] = 1
        self.uut.compute()
        res2 = self.uut.getData()
        self.assertTrue((res1!=res2).any())



    def test_2map(self):
        activation2 = np.zeros((self.size,self.size),np.intc)
        uut2 = NSpikeMap("uut2",self.size,activation=activation2)

        self.activation[2][5] = 1
        self.uut.compute()
        uut2.compute()
        res1 = self.uut.getData()
        res2 = uut2.getData()
        self.assertTrue(res1[0,0] != res2[0,0])










if __name__ == "__main__":
    unittest.main()
