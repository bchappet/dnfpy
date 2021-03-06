import unittest
import time
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
        self.assertEqual(res[5][5],0)
        self.assertEqual(res[6][5],1)
        self.assertEqual(res[5][6],1)
        self.assertEqual(res[4][5],1)
        self.assertEqual(res[5][4],1)
        self.uut.compute()#at last neigh cell receive bit
        res = self.uut.getData()
        self.assertEqual(res[6][5],2)
        self.assertEqual(res[5][6],2)
        self.assertEqual(res[4][5],2)
        self.assertEqual(res[5][4],2)

    def test_2activation(self):
        self.activation[4][5] = 1
        self.activation[5][4] = 1
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        res = self.uut.getData()
        self.assertEqual(res[5][5],1)

    def test_proba_0(self):
        self.uut.setParams(probaSynapse=0.)
        self.activation[2][5] = 1
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        res = self.uut.getData()
        self.assertEqual(res[2][5],0)
        self.assertEqual(res[0][0],0)



    def test_reset_data(self):
        self.uut.setParams(probaSpike=1.)
        self.activation[5][5] = 1
        self.uut.compute()
        self.activation[5][5] = 0
        for i in range(11):
            self.uut.compute()
        res = self.uut.getData()
        self.assertEqual(res[6,5] ,10)
        self.assertEqual(res[5,6] ,10)
        self.assertEqual(res[0,0] ,1)
        self.uut.resetData()
        self.uut.compute()
        self.assertEqual(res[6,5] ,1)
        self.assertEqual(res[5,6] ,1)
        self.assertEqual(res[0,0] ,1)
        for i in range(9):
            self.uut.compute()
        self.assertEqual(res[6,5] ,10)
        self.assertEqual(res[5,6] ,10)
        self.assertEqual(res[0,0] ,10)
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
        self.assertEqual(res[0,0] ,20)
        self.assertEqual(res[0,1] ,20)
        self.assertEqual(res[self.size-1,1] ,20)

    def test_100_computation_visual(self):
        sizeStream = 200
        self.size = 101
        self.activation = np.zeros((self.size,self.size),np.intc)
        self.uut = BsRsdnfMap("uut",self.size,activation=self.activation,routerType="uniformCell")
        self.uut.setParams(probaSpike=0.1)
        self.uut.setParams(sizeStream=sizeStream)
        self.uut.setParams(probaSynapse=0.98)
        self.uut.setParams(reproductible=True)

        sizePatch = 2
        for i in range(-1,sizePatch,1):
            for j in range(-1,sizePatch,1):
                self.activation[self.size//2+i][self.size//2+j] = 1;

        #10.331086 s before
        #7.96 after
        self.uut.setParams(nstep=sizeStream+self.size)
        start = time.clock()
        #for i in range(sizeStream+self.size):
        self.uut.compute()
        end = time.clock()
        print("Time elapsed %s"%(end-start))

        res = self.uut.getData()
        sumD = np.sum(res)
        self.assertEqual(553405,sumD)
        #view.plotArray(res)
        #view.show()

    def test_Precision2(self):
        self.uut.setParams(reproductible=True)
        self.uut.setParams(precisionProba=1)
        self.uut.setParams(probaSpike=0.4)
        self.activation[5][4] = 1
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        res = self.uut.getData()
        print( res)
        self.assertEqual(res[5][5],2)

    def test_Precision1(self):
        self.uut.setParams(precisionProba=1)
        self.uut.setParams(probaSpike=0.99999) #We cannot detect
        self.activation[5][4] = 1
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        res = self.uut.getData()
        #print res
        self.assertEqual(res[5][5],2)



    def test_Precision3(self):
        self.uut.setParams(probaSpike=0.9999)
        self.activation[5][4] = 1
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        self.uut.compute()
        res = self.uut.getData()
        #print res
        self.assertEqual(res[5][5],4)


if __name__ == "__main__":
    unittest.main()
