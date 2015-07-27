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
        def __init__(self,size,a,b,c,d):
            super(ExtensionMap2D_3,self).__init__("map",size=size,a=a,b=b,
                                                  c=c,d=d)
            self.child = ExtensionMap2D_2("name",size,c=c,d=d)
            self.addChildren(child=self.child)

        def _onParamsUpdate(self,a,b,c):
                a *=1.2
                b += 0.5
                c -= 10

                return dict(a=a,b=b,c=c)

        def _childrenParamsUpdate(self,c,d):
            self.child.setParams(c=c,d=d)

        def getChild(self):
            return self.child


class TestMap2DExtensions(unittest.TestCase):
        def setUp(self):
                pass
        def test_that_modification_happens(self):
                self.uut = ExtensionMap2D("name",10,dt=0.1,a=3,b=2)
                expected = (6,4)
                obtained = (self.uut.getArg('a'),self.uut.getArg('b'))
                self.assertEqual(expected,obtained)
        def test_that_modification_happens_also_if_constructor_param(self):
                self.uut = ExtensionMap2D("name",10,dt=0.1,a=3,b=2)
                expected = (6,4)
                obtained = (self.uut.getArg('a'),self.uut.getArg('b'))
                self.assertEqual(expected,obtained)

        def test_updateChildren_on_addChildren(self):
                #TODO update dnt modfify param with modified params
                uut = ExtensionMap2D_3(10,a=1,b=2,c=3,d=4)
                obtained = uut.getArgs('a','b','c','d')
                expected = dict(a=1.2,b=2.5,c=-7,d=4)
                self.assertEqual(expected,obtained)
                obtained = uut.getChild().getArgs('c','d')
                expected = dict(c=-14,d=6)
                self.assertEqual(expected,obtained)

        def _test_dont_update_children_on_param_update(self):
                #TODO update dnt modfify param with modified params
                uut = ExtensionMap2D_3(10,a=1,b=2,c=3,d=4)
                uut.setParams(c=12)
                obtained = uut.getArgs('a','b','c','d')
                expected = dict(a=1.2,b=2.5,c=2,d=4)
                self.assertEqual(expected,obtained)
                obtained = uut.getChild().getArgs('c','d')
                expected = dict(c=-14,d=6)
                self.assertEqual(expected,obtained)

        def _test_update_children_on_param_update_rec(self):
                uut = ExtensionMap2D_3(10,a=1,b=2,c=3,d=4)
                uut.setParams(c=12)
                obtained = uut.getArgs('a','b','c','d')
                expected = dict(a=1.2,b=2.5,c=2,d=4)
                self.assertEqual(expected,obtained)
                obtained = uut.getChild().getArgs('c','d')
                expected = dict(c=4,d=6)


if __name__ == '__main__':
        unittest.main()
