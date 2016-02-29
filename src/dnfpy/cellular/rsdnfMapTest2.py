
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
                self.uut.reset()

        def testSubsequenceInit(self):
            proba = self.uut.getArg('proba')
            self.assertEqual(proba,1)
            randomSequence2 = self.uut.getRandomSequence()
            self.assertEqual(np.sum(randomSequence2),self.size**2*4)

        def testSubsequence(self):
            proba = 0.8
            size = self.size
            randomSequence1 = (np.random.random((size,size,4)) <= proba).astype(np.intc)
            self.uut.setRandomSequence(randomSequence1)
            randomSequence2 = self.uut.getRandomSequence()
 
            self.assertTrue(np.array_equal(randomSequence1,randomSequence2))

                
        def testComputeP1(self):
            randomSequence = self.uut.getRandomSequence()
            self.activation[self.size//2,self.size//2] = 1
        
            for i in range(100):
                self.uut.compute()
                data = self.uut.getData()
            view.plotArray(data)
            view.show()
            self.assertEqual(data[self.size//2+1,self.size//2+1],20)

        def testComputeActivationNspike1(self):
            self.uut.setParams(nspike=1)
            self.activation[self.size//2,self.size//2] = 1
            for i in range(101):
                self.uut.compute()
            data = self.uut.getData()
            self.assertEqual(np.sum(data),self.size**2-1)

        def testComputeActivationNspike10(self):
            self.uut.setParams(nspike=10)
            self.activation[self.size//2,self.size//2] = 1
            for i in range(140):
                self.uut.compute()
            data = self.uut.getData()
            self.assertEqual(np.sum(data),10*(self.size**2)-10)

        def testComputeReset(self):
            self.uut.setParams(nspike=1)
            self.activation[self.size//2,self.size//2] = 1
            self.uut.setParams(proba=1.0)

            for i in range(5):
                self.uut.compute()
            data = self.uut.getData()
            self.assertEqual(data[self.size//2+4,self.size//2],1)
            self.assertEqual(data[self.size//2+5,self.size//2],0)

            self.uut.resetData()
            
            for i in range(5):
                self.uut.compute()
            data = self.uut.getData()
            self.assertEqual(data[self.size//2+4,self.size//2],1)
            self.assertEqual(data[self.size//2+5,self.size//2],0)


                


        
        def testMultiActivation(self):
            self.uut.setParams(nspike=9)
            self.activation[self.size//2,self.size//2] = 1
            self.activation[self.size//2,self.size//2+1] = 1
            self.activation[self.size//2+1,self.size//2+1] = 1
            self.activation[self.size//2+1,self.size//2] = 1
            self.uut.compute()
            self.activation[...] = 0
            for i in range(30):
                self.uut.compute()
            data = self.uut.getData()

        def testReset(self):
            self.uut.setParams(nspike=1)
            self.activation[self.size//2,self.size//2] = 1
            self.uut.compute()
            for i in range(20):
                self.uut.compute()
            data = self.uut.getData()
            self.uut.reset()
            data2 = self.uut.getData()
            self.assertEqual(np.sum(data2),0)

        def testComputeP2(self):
            self.activation[self.size//2,self.size//2] = 1
            self.uut.setParams(proba=0.99)
            for i in range(100):
                self.uut.compute()
            data = self.uut.getData()


        def tes_ComputePrecision(self):#TODO
            self.activation[self.size//2,self.size//2] = 1
            self.uut.setParams(proba=0.99)
            self.uut.setParams(precision=1)
            for i in range(100):
                self.uut.compute()
            data = self.uut.getData()
            view.plotArray(data)
            view.show()





               




if __name__ == "__main__":
        unittest.main()
