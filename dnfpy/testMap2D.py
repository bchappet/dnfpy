from unittest import TestCase
import unittest
from map2D import Map2D
import numpy as np
import copy
class TestMap2D(TestCase):

	
        
        def setUp(self):
        
                self.precision = 7
        
                self.size = 20
                self.dt = 0.1
                
                #Without children
                self.uut = Map2D(self.size,self.dt,{'a':1,'b':2})
                #with children
                self.uut_children = Map2D(self.size,self.dt*3,{'c':3,'d':4})
                self.uut_children.addChildren({'child1':self.uut,'child2':copy.deepcopy(self.uut)})
        
        def test_init(self):
                self.assertTrue(
                        (np.zeros((self.size,self.size),dtype=np.float32)==np.sum(self.uut.getData())).all(),
                        "The array should be initiated at 0")
                self.assertEqual(
                        self.dt,
                        self.uut.dt,
                        "Dt should be good")
                self.assertEqual(
                        self.size,
                        self.uut.size,
                        "Size should be good")
        def test_getNextUpdateTime(self):
                self.assertEqual(
                        0.1,
                        self.uut.getNextUpdateTime(),
                        "The next update time should be 0.1")
                        
                        
        def test_getSmallestNextUpdateTime(self):
                """ Method : getSmallestNextUpdateTime
                Scenario : no children"""
                self.assertEqual(
                        0.1,
                        self.uut.getSmallestNextUpdateTime(),
                        "The smallest next update time without children should be 0.1")
        
        def test_compute1(self):
                self.uut.compute()
                self.assertEqual(
                        1,
                        self.uut.nb_computation,
                        "The nb computation should be 1")
                        
        def test_update1(self):
                """Method: update
                Scenario: the simuTime is exactly the nextSimuTime, there is 1 computation"""
                self.uut.update(0.1)
                self.assertEqual(
                        1,
                        self.uut.nb_computation,
                        "The nb computation should be 1")
        
        def test_update_to_small1(self):
                """Method: update
                Scenario: the simuTime is to small, there is no computation"""
                self.uut.update(0.01)
                self.assertEqual(
                        0,
                        self.uut.nb_computation,
                        "The nb computation should be 0")
        
        def test_update_to_big1(self):
                """Method: update
                Scenario: the simuTime is to big, an AssertionError is throw"""
                with self.assertRaises(AssertionError): 
                        self.uut.update(1)
                        
        #test params
        def test_params(self):
                self.assertEqual(1,self.uut.globalRealParams['a'],"params should be the same")
                
        def test_updateParams(self):
                self.uut.updateParams({'new':10,'a':100})
                self.assertEqual(100,self.uut.globalRealParams['a'],"params should be updated")
        
        #With children
        def test_addChildren(self):
                self.assertEqual(
                        self.uut,
                        self.uut_children.children['child1'],
                        "The first child1 should be the same")
                        
        def test_update2(self):
                """Method: update
                Scenario: 
                1)   time 0.1, only the children should be updated 
                2)   time 0.2, only the children should be updated 
                3)   time 0.3, child and father are updated 
                4)   time 0.4, only the children should be updated """
                self.uut_children.update(0.1)
                self.assertEqual(
                        1,
                        self.uut_children.children['child1'].nb_computation,
                        "The nb computation for children should be 1")
                self.assertEqual(
                        0,
                        self.uut_children.nb_computation,
                        "The nb computation for uut_children should be 0")
                        
                self.uut_children.update(0.2)
                self.assertEqual(
                        2,
                        self.uut_children.children['child1'].nb_computation,
                        "The nb computation for children should be 2")
                self.assertEqual(
                        0,
                        self.uut_children.nb_computation,
                        "The nb computation for uut_children should be 0")
                        
                self.uut_children.update(0.3)
                self.assertEqual(
                        3,
                        self.uut_children.children['child1'].nb_computation,
                        "The nb computation for children should be 3")
                self.assertEqual(
                        1,
                        self.uut_children.nb_computation,
                        "The nb computation for uut_children should be 1")
        def test_getTime(self):
            """Method getTime
            Scenario : the time should be rounded after 3 update"""
            self.uut.update(0.1)
            self.uut.update(0.2)
            self.uut.update(0.30000000000000001)
            obtained = self.uut.getTime()
            self.assertAlmostEqual(0.3,obtained,self.precision,"the result should be the same")
                
                
if __name__ == '__main__':
        unittest.main(7)
        
