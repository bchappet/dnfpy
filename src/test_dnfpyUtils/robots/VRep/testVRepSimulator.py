from dnfpyUtils.robots.VRep.vRepSimulator import VRepSimulator
import unittest

class TestVRepSimulator(unittest.TestCase):
    def setUp(self):
        self.uut=VRepSimulator("uut", 1, 0.1)
        
    def testConnectionError(self):
        self.uut.port=19999
        self.assertRaises(IOError, self.uut.connection)
        
    def testConnectionOk(self):
        self.uut.port=19999
        self.assertNotEquals(self.uut.clientID,-1)
        
if __name__ == '__main__':
    unittest.main()
        