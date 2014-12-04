import unittest
from dnfpy.core.map2D import Map2D

class ExtensionMap2D(Map2D):
        def _onParamsUpdate(self,a,b):
                a *=2
                b += 2
                return dict(a=a,b=b)


class ExtensionMap2D_2(Map2D):
        def _onParamsUpdate(self,c,d):
                c *=2
                d += 2
                return dict(c=c,d=d)


class ExtensionMap2D_3(Map2D):
        def _onParamsUpdate(self,a,b):
                a *=1.2
                b += 0.5
                return dict(a=a,b=b)


class TestMap2DExtensions(unittest.TestCase):
        def setUp(self):
                pass
        def test_that_modification_happens(self):
                self.uut = ExtensionMap2D(10,dt=0.1,a=3,b=2)
                expected = (6,4)
                obtained = (self.uut.getArg('a'),self.uut.getArg('b'))
                self.assertEqual(expected,obtained)
        def test_that_modification_happens_also_if_constructor_param(self):
                self.uut = ExtensionMap2D(10,dt=0.1,a=3,b=2)
                expected = (6,4)
                obtained = (self.uut.getArg('a'),self.uut.getArg('b'))
                self.assertEqual(expected,obtained)



if __name__ == '__main__':
        unittest.main()
