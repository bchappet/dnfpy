import unittest
import numpy as np
from casasMap import CasasMap
from dnfpy.core.constantMap import ConstantMap

class CasasMapTest(unittest.TestCase):
        def setUp(self):
                self.size = 2000
                self.activation = np.zeros((self.size,self.size),np.bool_)
                self.uut = CasasMap("uut",self.size,activation=self.activation)

        def testConstruct(self):
                print self.uut
        
        def testCompute(self):
                for i in range(100):
                    self.uut.compute()
                print self.uut
                




if __name__ == "__main__":
        unittest.main()
