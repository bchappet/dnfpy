import unittest
import numpy as np
from dnfpy.cellular.bsRsdnfMap import BsRsdnfMap
import dnfpy.view.staticViewMatplotlib as view

class TestBsRsdnfMap(unittest.TestCase):
    def setUp(self):
        self.size = 11
        self.activation = np.zeros((self.size,self.size),np.intc)
        self.uut = BsRsdnfMap("uut",self.size,activation=self.activation)

    def test_update(self):
        self.uut.compute()
        data = self.uut.getData()
        self.assertEqual(np.sum(data),0)

    def test_activation(self):
        self.activation[5][5] = 1
        self.uut.compute()#set regState 1 in cell
        self.uut.compute()#router of cel set state 1
        self.uut.compute()#at last neigh cell receive bit
        res = self.uut.getData()
        self.assertEquals(res[5][5],0)
        self.assertEquals(res[6][5],1)
        self.assertEquals(res[5][6],1)
        self.assertEquals(res[4][5],1)
        self.assertEquals(res[5][4],1)
        self.uut.compute()#at last neigh cell receive bit
        res = self.uut.getData()
        self.assertEquals(res[6][5],2)
        self.assertEquals(res[5][6],2)
        self.assertEquals(res[4][5],2)
        self.assertEquals(res[5][4],2)

    def test_2activation(self):
        self.activation[4][5] = 1
        self.activation[5][4] = 1
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        res = self.uut.getData()
        self.assertEquals(res[5][5],2)

    def test_proba_0(self):
        self.uut.setParams(probaSynapse=0.)
        self.activation[2][5] = 1
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        res = self.uut.getData()
        self.assertEquals(res[2][5],0)
        self.assertEquals(res[0][0],0)

    def test_reset_data(self):
        self.uut.setParams(probaSpike=1.)
        self.activation[5][5] = 1
        self.uut.compute()
        self.activation[5][5] = 0
        for i in range(11):
            self.uut.compute()
        res = self.uut.getData()
        self.assertEquals(res[6,5] ,10)
        self.assertEquals(res[5,6] ,10)
        self.assertEquals(res[0,0] ,1)
        self.uut.resetData()
        self.uut.compute()
        self.assertEquals(res[6,5] ,1)
        self.assertEquals(res[5,6] ,1)
        self.assertEquals(res[0,0] ,1)
        for i in range(9):
            self.uut.compute()
        self.assertEquals(res[6,5] ,10)
        self.assertEquals(res[5,6] ,10)
        self.assertEquals(res[0,0] ,10)
        for i in range(10):
            self.uut.compute()

    def test_100_computation(self):
        self.uut.setParams(probaSpike=1.)
        self.activation[5][5] = 1
        self.uut.compute()
        self.activation[5][5] = 0
        for i in range(1000):
            self.uut.compute()
        res = self.uut.getData()
        self.assertEquals(res[0,0] ,20)
        self.assertEquals(res[0,1] ,20)
        self.assertEquals(res[self.size-1,1] ,20)

    def test_100_computation_visual(self):
        self.size = 101
        self.activation = np.zeros((self.size,self.size),np.intc)
        self.uut = BsRsdnfMap("uut",self.size,activation=self.activation)
        self.uut.setParams(probaSpike=0.01)
        self.uut.setParams(sizeStream=1000)
        self.uut.setParams(probaSynapse=0.99)
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                self.activation[self.size/2+i][self.size/2+j] = 1;
        self.uut.compute()
        self.activation = np.zeros((self.size,self.size),np.intc)
        for i in range(1000):
            self.uut.compute()

        res = self.uut.getData()
        print res
        view.plotArray(res)
        view.show()


if __name__ == "__main__":
    unittest.main()
