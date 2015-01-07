import unittest
import numpy as np
from hardlib import HardLib


class TestHardLibParameters(unittest.TestCase):
    def setUp(self):
        self.size = 11
        self.lib = HardLib(self.size,self.size,"cellnspike","nspikeconnecter")

    def test_set_map_param(self):
        self.lib.setMapParam(0,30)
        self.assertTrue(self.lib.getMapParam(0,int) == 30)


if __name__ == "__main__":
    unittest.main()

