import unittest
from testMap2D import TestMap2D
from testMap2DExtensions import TestMap2DExtensions
from testUtils import TestUtils
from testFuncMap2D import TestFuncMap2D
from testFuncWithoutKeywords import TestFuncWithoutKewords
from testInputMap import TestInputMap
from testFieldMap import TestFieldMap

def suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMap2D))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMap2DExtensions))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUtils))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFuncMap2D))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFuncWithoutKewords))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestInputMap))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFieldMap))

        return suite

if __name__ == '__main__':
        test_suite = suite()
        unittest.main()

