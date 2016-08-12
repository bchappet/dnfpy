from dnfpy.core.constantMap import ConstantMap
import unittest
import numpy as np
import dnfpy.view.staticViewMatplotlib as view
from dnfpy.cellular.rsdnf2LayerConvolution import Rsdnf2LayerConvolution
import matplotlib.pyplot as plt

class Rsdnf2LayerConvolutionTest(unittest.TestCase):
        def setUp(self):
                self.size = 100
                self.activation = np.zeros((self.size,self.size),np.intc)
                self.uut = Rsdnf2LayerConvolution("uut",self.size,activation=self.activation)
                self.uut.reset()
                self.activation[self.size//2,self.size//2] = 1
                self.uut.setParams(pExc=1.0,pInh=1.0,nspike=20)


#        def testConvolution1(self):
#            self.uut.setParams(shift=1)
#            self.uut.setParams(nspike=200,iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.4)
#            for i in range(200):
#                self.uut.compute()
#            data = self.uut.getData()
#            view.plotArray(data)
#            view.show()

        def testResetLat(self):
            """
            Check that everything is reset after call to reset lat
            """
            self.uut.setParams(nspike=2000,iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.4)
            for i in range(120):
                self.uut.compute()
            data = self.uut.getData()

            self.activation[...] = 0
            self.uut.resetLat()
            for i in range(120):
                self.uut.compute()
            data = self.uut.getData()
            assert(np.sum(data) == 0)



           


        
        def testComputeP1(self):
            for i in range(120):
                self.uut.compute()
                data = self.uut.excMap
            self.assertEqual(data[self.size//2+1,self.size//2+1],20)

#        def testWorstCaseScenario(self):
#            self.activation[self.size//2-5:self.size//2+5,self.size//2-5:self.size//2+5] = 1
#            self.uut.setParams(nspike=20)
#        
#            for i in range(100*20 + 200):
#                self.uut.compute()
#                data = self.uut.excMap
#            self.assertEqual(np.sum(data),100*100*100*20 - 100*20)

        def testComputeActivationNspike1(self):
            self.uut.setParams(nspike=1)
            self.activation[self.size//2,self.size//2] = 1
            for i in range(102):
                self.uut.compute()
            data = self.uut.excMap
            self.assertEqual(np.sum(data),self.size**2-1)

        def testComputeActivationNspike10(self):
            self.uut.setParams(nspike=10)
            self.activation[self.size//2,self.size//2] = 1
            for i in range(140):
                self.uut.compute()
            data = self.uut.excMap
            self.assertEqual(np.sum(data),10*(self.size**2)-10)

#        def testComputeReset(self):
#            self.uut.setParams(nspike=1)
#            self.activation[self.size//2,self.size//2] = 1
#            self.uut.setParams(proba=1.0)
#
#            for i in range(6):
#                self.uut.compute()
#            data = self.uut.excMap
#            self.assertEqual(data[self.size//2+4,self.size//2],1)
#            self.assertEqual(data[self.size//2+5,self.size//2],0)
#
#            self.uut.resetLat()
#            
#            for i in range(5):
#                self.uut.compute()
#            data = self.uut.excMap
#            self.assertEqual(data[self.size//2+4,self.size//2],1)
#            self.assertEqual(data[self.size//2+5,self.size//2],0)
#
#        
#        def testMultiActivation(self):
#            self.uut.setParams(nspike=9)
#            self.activation[self.size//2,self.size//2] = 1
#            self.activation[self.size//2,self.size//2+1] = 1
#            self.activation[self.size//2+1,self.size//2+1] = 1
#            self.activation[self.size//2+1,self.size//2] = 1
#            self.uut.compute()
#            self.activation[...] = 0
#            for i in range(30):
#                self.uut.compute()
#            data = self.uut.excMap
#
#        def testReset(self):
#            self.uut.setParams(nspike=1)
#            self.activation[self.size//2,self.size//2] = 1
#            self.uut.compute()
#            for i in range(20):
#                self.uut.compute()
#            data = self.uut.excMap
#            self.uut.reset()
#            data2 = self.uut.getData()
#            self.assertEqual(np.sum(data2),0)
#
#        def testComputeP2(self):
#            self.activation[self.size//2,self.size//2] = 1
#            self.uut.setParams(proba=0.99)
#            for i in range(100):
#                self.uut.compute()
#            data = self.uut.excMap
#
#
#        def tes_ComputePrecision(self):#TODO
#            self.activation[self.size//2,self.size//2] = 1
#            self.uut.setParams(proba=0.99)
#            self.uut.setParams(precision=1)
#            for i in range(100):
#                self.uut.compute()
#            data = self.uut.excMap
#            view.plotArray(data)
#            view.show()
#
#
#
#
if __name__ == "__main__":
        unittest.main()
