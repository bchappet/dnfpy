import unittest
import numpy as np
from hardlib import HardLib

class TestHardLib(unittest.TestCase):
    def setUp(self):
        self.size = 11
        self.lib = HardLib(self.size,self.size,"cellnspike","nspikeconnecter")

    def test_set_get_cell_attribute(self):
        self.lib.setCellAttribute(0,0,0,10)
        attr = self.lib.getCellAttribute(0,0,0,int)
        self.assertTrue(attr == 10)

    def test_get_array_attribute(self):
        self.lib.setCellAttribute(4,2,0,10)
        arr = np.ones((self.size,self.size),dtype=np.intc)
        self.lib.getArrayAttribute(0,arr)
        self.assertTrue(arr[2][4] == 10)

    def test_set_array_attributes(self):
        arr = np.ones((self.size,self.size),dtype=np.intc)
        arr[2][5] = 23
        self.lib.setArrayAttribute(0,arr)
        res = np.zeros((self.size,self.size),dtype=np.intc)
        self.lib.getArrayAttribute(0,res)
        self.assertTrue(res[2][5] == 23)
        self.assertTrue(res[0][0] == 1)

if __name__ == "__main__":
    unittest.main()

