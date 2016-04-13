import unittest
import time
import numpy as np
from dnfpy.cellular.hardlib import HardLib

ACTIVATED = 2
NB_BIT_RECEIVED = 1
class TestHardLib(unittest.TestCase):
    def setUp(self):
        self.size = 11
        self.lib = HardLib(self.size,self.size,"cellbsrsdnf","rsdnfconnecter")
        self.lib.initSeed(255)

    def test_defaultParameters(self):
        # We assert the spike out of the default param
        self.assertEqual(1,self.lib.getMapParam(0,float)) #PROBA_SPIKE
        self.assertEqual(20,self.lib.getMapParam(1,int)) #SIZE_STREAM
        self.assertEqual(1,self.lib.getMapSubParam(0,float)) #PROBA_SYNAPSE


    def test_activate(self):
        self.activate()

        hsize = self.size//2
        activation = self.getArrayZero(np.intc)
        self.lib.getRegArray(ACTIVATED,activation)
        print(activation)
        self.assertTrue(activation[hsize,hsize])
        self.assertTrue(activation[hsize+2,hsize+2])
        self.assertTrue(activation[hsize,hsize-2])


    def getArrayZero(self,dtype):
        return np.zeros((self.size,self.size),dtype=dtype)


    def test_compute(self):
        hsize = self.size//2
        self.activate()

        start = time.clock()
        for i in range(20 + 2*self.size-1+500):
            self.lib.step()
        end = time.clock()
        print("elapsed step : %s"%(end-start))

        nbBitReceived = self.getArrayZero(np.intc)
        self.lib.getRegArray(NB_BIT_RECEIVED,nbBitReceived)
        print(nbBitReceived)
        self.assertEqual(nbBitReceived[hsize,hsize-1],24)
        self.assertEqual(nbBitReceived[hsize,hsize+1],22)
        self.assertEqual(nbBitReceived[hsize-1,hsize],24)
        self.assertEqual(nbBitReceived[hsize+1,hsize],22)

    def test_nstep(self):
        hsize = self.size//2
        self.activate()
        start = time.clock()
        self.lib.nstep(20+2*self.size-1+500)
        end = time.clock()
        print("elapsed nstep : %s"%(end-start))
        nbBitReceived = self.getArrayZero(np.intc)
        self.lib.getRegArray(NB_BIT_RECEIVED,nbBitReceived)
        print(nbBitReceived)
        self.assertEqual(nbBitReceived[hsize,hsize-1],24)
        self.assertEqual(nbBitReceived[hsize,hsize+1],22)
        self.assertEqual(nbBitReceived[hsize-1,hsize],24)
        self.assertEqual(nbBitReceived[hsize+1,hsize],22)




    def activate(self):
        hsize = self.size//2
        self.lib.setRegCell(hsize,hsize,ACTIVATED,1)
        self.lib.setRegCell(hsize+2,hsize+2,ACTIVATED,1)
        self.lib.setRegCell(hsize-2,hsize,ACTIVATED,1)
        self.lib.synch()






if __name__ == "__main__":
    unittest.main()

