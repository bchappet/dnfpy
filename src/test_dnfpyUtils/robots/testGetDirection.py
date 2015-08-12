from dnfpyUtils.robots.VRep.vRepSimulator import VRepSimulator
from dnfpyUtils.robots.getDirection import GetDirection
import unittest

import math
class TestGetDirection(unittest.TestCase):
    def setUp(self):
        self.uut=VRepSimulator("uut", 1, 0.1)
        self.uut.synchronous=True
        self.uut.port=19997
        self.uut.connection()
        self.vvt=GetDirection("vvt",8)
        self.vvt.addChildren(simulator=self.uut)
        
    def testCompute1(self):
        
        a=0
        beta=0
        
        self.vvt.compute()
        beta=self.vvt.getData()
        print("position",beta)
        self.assertNotEquals(a,beta.any())
        self.uut.disconnection()
    
        
        
if __name__ == '__main__':
    unittest.main()
        
