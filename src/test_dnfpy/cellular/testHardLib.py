import unittest
import time
import numpy as np
from dnfpy.cellular.hardlib import HardLib

class TestHardLib(unittest.TestCase):
    def setUp(self):
        self.size = 11
        self.lib = HardLib(self.size,self.size,"cellbsrsdnf","rsdnfconnecter")
        self.lib.initSeed(255)

    def test_defaultParameters(self):
        # We assert the spike out of the default param
        self.assertEquals(1,self.lib.getMapParam(0,float)) #PROBA_SPIKE
        self.assertEquals(20,self.lib.getMapParam(1,int)) #SIZE_STREAM
        self.assertEquals(1,self.lib.getMapParam(2,float)) #PROBA_SYNAPSE


    def test_activate(self):
        self.activate()
        hsize = self.size/2
        activation = self.getArrayZero(np.bool)
        self.lib.getArrayAttribute(1,activation)
        print(activation)
        self.assertTrue(activation[hsize,hsize])
        self.assertTrue(activation[hsize+2,hsize+2])
        self.assertTrue(activation[hsize,hsize-2])


    def getArrayZero(self,dtype):
        return np.zeros((self.size,self.size),dtype=dtype)


    def test_compute(self):
        hsize = self.size/2
        self.activate()

        start = time.clock()
        for i in range(20 + 2*self.size-1+500):
            self.lib.step()
        end = time.clock()
        print("elapsed step : %s"%(end-start))

        nbBitReceived = self.getArrayZero(np.intc)
        self.lib.getArrayAttribute(0,nbBitReceived)
        print(nbBitReceived)
        self.assertEquals(nbBitReceived[hsize,hsize-1],24)
        self.assertEquals(nbBitReceived[hsize,hsize+1],22)
        self.assertEquals(nbBitReceived[hsize-1,hsize],24)
        self.assertEquals(nbBitReceived[hsize+1,hsize],22)

    def test_nstep(self):
        hsize = self.size/2
        self.activate()
        start = time.clock()
        self.lib.nstep(20+2*self.size-1+500)
        end = time.clock()
        print("elapsed nstep : %s"%(end-start))
        nbBitReceived = self.getArrayZero(np.intc)
        self.lib.getArrayAttribute(0,nbBitReceived)
        print(nbBitReceived)
        self.assertEquals(nbBitReceived[hsize,hsize-1],24)
        self.assertEquals(nbBitReceived[hsize,hsize+1],22)
        self.assertEquals(nbBitReceived[hsize-1,hsize],24)
        self.assertEquals(nbBitReceived[hsize+1,hsize],22)




    def activate(self):
        hsize = self.size/2
        self.lib.setCellAttribute(hsize,hsize,1,True)
        self.lib.setCellAttribute(hsize+2,hsize+2,1,True)
        self.lib.setCellAttribute(hsize-2,hsize,1,True)






if __name__ == "__main__":
    unittest.main()

