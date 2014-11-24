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


                


                
                

if __name__ == '__main__':
        unittest.main()

