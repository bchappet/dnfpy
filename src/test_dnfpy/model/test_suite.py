import unittest
from test_dnfpy.model import *
def suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestInputMap))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFieldMap))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestLateralWeightsMap))

        return suite

if __name__ == '__main__':
        test_suite = suite()
        unittest.main()

