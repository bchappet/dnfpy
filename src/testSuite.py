import unittest
from dnfpy_tests import *

def suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMap2D))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMap2DExtensions))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUtils))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFuncMap2D))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFuncWithoutKewords))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestInputMap))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFieldMap))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestLateralWeightsMap))

        return suite

if __name__ == '__main__':
        test_suite = suite()
        unittest.main()

