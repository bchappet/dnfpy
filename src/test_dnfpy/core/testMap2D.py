#-*- coding: utf-8 -*-
from unittest import TestCase
import unittest
from dnfpy.core.map2D import Map2D
import numpy as np
import copy
class TestMap2D(TestCase):
        def setUp(self):
            self.precision = 7
            self.size= 20
            self.dt =0.1
            #Without children
            self.uut = Map2D(size=self.size,dt=self.dt,a=1,b=2)
            #with children
            self.uut_children = Map2D(size=self.size,dt=self.dt*3,c=3,d=4)
            self.uut_children.addChildren(child1=self.uut,child2=copy.deepcopy(self.uut))

        def test_init(self):
                self.assertTrue(
                        (np.zeros((self.size,self.size),dtype=np.float32)==np.sum(self.uut.getData())).all(),
                        "The array should be initiated at 0")

        def test_getSmallestNextUpdateTime(self):
                """ Method : getSmallestNextUpdateTime
                Scenario : no children"""
                self.assertEqual(
                        0.1,
                        self.uut.getSmallestNextUpdateTime(),
                        "The smallest next update time without children should be 0.1")

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
                        self.uut.nb_computation,
                        "The nb computation for children should be 1")
                self.assertEqual(
                        0,
                        self.uut_children.nb_computation,
                        "The nb computation for uut_children should be 0")

                self.uut_children.update(0.2)
                self.assertEqual(
                        2,
                        self.uut.nb_computation,
                        "The nb computation for children should be 2")
                self.assertEqual(
                        0,
                        self.uut_children.nb_computation,
                        "The nb computation for uut_children should be 0")

                self.uut_children.update(0.3)
                self.assertEqual(
                        3,
                        self.uut.nb_computation,
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
        def test_reset(self):
            """Method reset"""
            self.uut.update(0.1)
            self.uut.update(0.2)
            self.uut.reset()
            self.assertTrue(
                    (np.zeros((self.size,self.size),dtype=np.float32)==np.sum(self.uut.getData())).all(),
                    "The array should be reset at 0")
        def test_init_size1(self):
            """Init
            With a size 1. data should be a real"""
            test = Map2D(size=1,dt=self.dt)
            self.assertEqual(0.,test.getData(),"When initiated with a size == 1, the data should be a real")
        def test_arg_init(self):
            self.uut.update(0.1)
            expected = dict(size=self.size,dt=self.dt,a=1,b=2,time=0.1)
            obtained = self.uut.last_computation_dictionary
            self.assertEqual(expected,obtained,"result should be the same")

        def test_get_children_names(self):
            obtained = self.uut_children.getChildrenNames()
            expected = set(['child1','child2'])
            self.assertEqual(expected,obtained,"result should be the same")
        def test_get_attributes_names(self):
            obtained = self.uut.getAttributesNames()
            expected = set(['time','size','dt','a','b'])
            self.assertEqual(expected,obtained,"result should be the same")
        def test_children_cout(self):
            self.assertEqual(2,self.uut_children.getChildrenCount())
        def test_remove_children(self):
            self.uut_children.removeChild('child2')
            self.assertEqual(1,self.uut_children.getChildrenCount())
        def test_artificial_computation(self):
            self.uut_children.compute()
            self.assertEqual(1,self.uut_children.nb_computation)
            self.assertEqual(1,self.uut.nb_computation)
            self.assertEqual(0.0,self.uut_children.getTime())
            self.assertEqual(0.0,self.uut.getTime())

if __name__ == '__main__':
        unittest.main()

