import unittest
from test_dnfpy.core import *
def suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMap2D))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMap2DExtensions))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUtils))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFuncMap2D))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFuncWithoutKewords))

        return suite

if __name__ == '__main__':
        test_suite = suite()
        unittest.main()

