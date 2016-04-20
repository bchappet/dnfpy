import unittest
from spso2006 import Spso

class Spso2006_t(unittest.TestCase):
    
    def testConstructNeighbor(self):
        uut = Spso(20);
        print(uut.nbNeigh)
        print(uut.neighs)
        print(uut.l)

    def testReconstructNeighbor(self):
        uut = Spso(20)
        print(uut.bestF)
        uut.updatePart(0)
        print(uut.bestF)
        uut.updatePart(1)
        print(uut.bestF)
        
        

if __name__ == "__main__":
    unittest.main()
