import unittest
import numpy as np
from hardlib import HardLib

class TestHardLib(unittest.TestCase):
    def setUp(self):
        self.size = 11
        self.lib = HardLib(self.size,self.size,"cellrsdnf","rsdnfconnecter")

    def test_get_reg_array_int(self):
        array = np.ones((self.size,self.size),dtype=np.intc)
        self.lib.getRegArray(0,array)
        self.assertTrue(np.sum(array) == 0)

    def test_get_reg_array_bool(self):
        array = np.ones((self.size,self.size),dtype=np.bool)
        self.lib.getRegArray(1,array)
        self.assertTrue(np.sum(array) == False)

    def test_set_reg_int(self):
        array = np.ones((self.size,self.size),dtype=np.intc)
        self.lib.setRegCell(4,3,0,21)
        self.lib.synch()
        self.lib.getRegArray(0,array)
        self.assertTrue(array[3][4] == 21)





if __name__ == "__main__":
    unittest.main()

