import unittest
from dnfpy.model.fieldMap import FieldMap


class TestFieldMap(unittest.TestCase):
        def setUp(self):
                self.uut = FieldMap(size=1,dt=0.1,lat=1,aff=1,tau=0.8,h=0,th=0.64)
                self.uut.registerOnGlobalParamsChange(model='model')
                self.globalParams = {'model':'cnft'}
                self.uut.updateParams(self.globalParams)

        def test_update(self):
                self.uut.update(0.1)
                obtained = self.uut.getData()
                expected = 0.25
                self.assertEqual(obtained,expected)
        def test_update2(self):
                self.uut.update(0.1)
                self.uut.update(0.2)
                obtained = self.uut.getData()
                expected =  0.46875
                self.assertEqual(obtained,expected)
        def test_update_spike(self):
                self.globalParams = {'model':'spike'}
                self.uut.updateParams(self.globalParams)
                self.uut.update(0.1)
                obtained = self.uut.getData()
                expected =  1.375
                self.assertEqual(obtained,expected)
        def test_update_spike(self):
                self.globalParams = {'model':'spike'}
                self.uut.updateParams(self.globalParams)
                self.uut.update(0.1)
                self.uut.update(0.2)
                obtained = self.uut.getData()
                expected =  0.234375
                self.assertEqual(obtained,expected)




        


if __name__ == "__main__":
        unittest.main()


