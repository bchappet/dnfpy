import unittest
import time
import numpy as np
from dnfpy.cellular.sbsFastMap import SbsFastMap
from dnfpy.core.constantMap import ConstantMap

class TestSpeedSBSFast(unittest.TestCase):
    def setUp(self):
        self.size = 101
        self.hsize = self.size//2
        self.uut = SbsFastMap("uut",self.size)
        self.uut.lib.initSeed(255)
        self.activation = np.zeros((self.size,self.size),np.intc)
        activationMap = ConstantMap("actmap",self.size, self.activation)
        self.uut.addChildren(activation=activationMap)

    def test_speed_step1(self):
        self.uut.setParams(sizeStream=1000)
        start = time.clock()
        for i in range(20):
            self.activate2()
            self.uut.compute()
            print("step %s"%i)

        end = time.clock()
        print("elapsed time %s"%(end-start))
        data =  self.uut.getData()
        self.assertEqual(data[0,0] ,1000)

    def test_speed_step2(self):
        self.uut.setParams(sizeStream=500,probaSpike=0.1,probaSynapse=0.99)
        start = time.clock()
        for i in range(3):
            self.activate2()
            self.uut.compute()
            print("step %s"%i)

        end = time.clock()
        print("elapsed time %s"%(end-start))
        data =  self.uut.getData()
        print(data)




    def activate1(self):
        self.activation[self.hsize,self.hsize]=1
        self.activation[self.hsize+2,self.hsize+2]=1
        self.activation[self.hsize,self.hsize-2]=1

    def activate2(self):
          for i in range(-2,3,1):
            for j in range(-2,3,1):
                self.activation[self.size//2+i][self.size//2+j] = 1;




if __name__ == "__main__":
    unittest.main()
