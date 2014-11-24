import unittest
from map2D import Map2D

class ExtensionMap2D(Map2D):
        def _modifyParams(self,params,globalParams):
                params['a'] *=2
                params['b'] += 2
        def getParam(self,key):
                return self._getArg(key)

class ExtensionMap2D_2(Map2D):
        def _modifyParams(self,params,globalParams):
                params['c'] *=2
                params['d'] += 2
        def getParam(self,key):
                return self._getArg(key)
class ExtensionMap2D_modifRecursif(Map2D):
        def _modifyParamsRecursively(self,params):
                params['a'] += 100
                params['d'] /= 10.
        def _modifyParams(self,params,globalParams):
                params['a'] *=2
                params['b'] += 2
        def getParam(self,key):
                return self._getArg(key)





class TestMap2DExtensions(unittest.TestCase):
        def setUp(self):
                pass
        def test_that_modification_happens(self):
                self.uut = ExtensionMap2D(10,dt=0.1,a=3)
                globalParams = dict(a=4,b=2)
                self.uut.registerOnGlobalParamsChange(a='a',b='b')
                self.uut.updateParams(globalParams)
                expected = (8,4)
                obtained = (self.uut.getParam('a'),self.uut.getParam('b'))
                self.assertEqual(expected,obtained)
        def test_exception_key_error(self):
                self.uut = ExtensionMap2D_2(10,dt=0.1,a=3)
                globalParams = dict(a=4,c=2)
                self.uut.registerOnGlobalParamsChange(a='a',b='c')
                with self.assertRaises(KeyError):
                    self.uut.updateParams(globalParams)
        def test_key_error_when_key_is_not_in_globalParams(self):
                self.uut = ExtensionMap2D(10,dt=0.1)
                globalParams = dict(b=4)
                self.uut.registerOnGlobalParamsChange(b='b')
                with self.assertRaises(KeyError):
                    self.uut.updateParams(globalParams)
        def test_that_modification_happens_also_if_constructor_param(self):
                self.uut = ExtensionMap2D(10,dt=0.1,a=3)
                self.uut.registerOnGlobalParamsChange(b='b')
                globalParams = dict(b=2)
                self.uut.updateParams(globalParams)
                expected = (6,4)
                obtained = (self.uut.getParam('a'),self.uut.getParam('b'))
                self.assertEqual(expected,obtained)
        def test_modif_recursif_computation_order(self):
                """
                    Method: _modifyParamsRecursively
                    Scenario: Order of computation respected
                """
                self.uut = ExtensionMap2D_modifRecursif(10,dt=0.1,a=3,b=2)
                child1 = ExtensionMap2D(10,dt=0.1)
                child1.registerOnGlobalParamsChange(a='a',b='b')
                child2 = ExtensionMap2D_2(10,dt=0.1,c=3)
                child2.registerOnGlobalParamsChange(d='d')
                self.uut.addChildren(child1=child1,child2=child2)
                globalParams = dict(a=4,b=2,d=0.2)
                self.uut.updateParams(globalParams)

                self.assertEqual(child1.getParam('a'),(4+100)*2, \
                                "The order of execution is _modifyParamsRecursively and then local _modifyParams ")
                self.assertEqual(child1.getParam('b'),4,\
                                "Only the local _modifyParams is executed ")
                self.assertEqual(child2.getParam('c'),3*2,\
                                "The behaviour is different for a construction param TODO fix shoudl be 3*2*250")
                self.assertEqual(child2.getParam('d'),(0.2/10 + 2),\
                                "The order should be respected")
        def test_modif_recursif_apply_on_self_with_the_same_order(self):
                """
                    Method: _modifyParamsRecursively
                    Scenario: Order of computation respected on self
                """
                self.uut = ExtensionMap2D_modifRecursif(10,dt=0.1,a=3)
                self.uut.registerOnGlobalParamsChange(b='b',c='c')
                globalParams = dict(a=4,b=2,c=1.2,d=0.2)
                self.uut.updateParams(globalParams)
                self.assertEqual(self.uut.getParam('a'),3*2, \
                                "We did not register a for change")
                self.assertEqual(self.uut.getParam('b'),(2+2))
                self.assertEqual(self.uut.getParam('c'),(1.2))
        def test_modif_recursif_does_not_alter_globalParam(self):
                """
                    Method: _modifyParamsRecursively
                    Scenario: Order of computation respected on self
                """
                self.uut = ExtensionMap2D_modifRecursif(10,dt=0.1,a=3)
                self.uut.registerOnGlobalParamsChange(b='b',c='c')
                globalParams = dict(a=4,b=2,c=1.2,d=0.2)
                saveGlobalParams = dict(**globalParams)
                self.uut.updateParams(globalParams)
                self.assertEqual(globalParams,saveGlobalParams, \
                                "The globalParams should not be altered by the process")




if __name__ == '__main__':
        unittest.main()

