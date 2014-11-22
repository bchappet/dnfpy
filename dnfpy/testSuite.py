import unittest
from testMap2D import TestMap2D
from testUtils import TestUtils
from testFuncMap2D import TestFuncMap2D
from testFuncWithoutKeywords import TestFuncWithoutKewords

def suite():
	suite = unittest.TestSuite()
	suite.addTest(TestMap2D())
	suite.addTest(TestUtils())
	suite.addTest(TestFuncMap2D())
	suite.addTest(TestFuncWithoutKewords())

	return suite

if __name__ == '__main__':
	test_suite = suite()
	unittest.main()

