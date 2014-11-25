import unittest
from dnfpy.model.activationMap import ActivationMap

class TestActivationMap(unittest.TestCase):
    def test_cnft_normal(self):
        self.uut = ActivationMap(size=1,dt=0.1,model='cnft',field=1,th=0.75)
        self.uut.update(0.1)
        self.assertEqual(1,self.uut.getData())
    def test_cnft_negative(self):
        self.uut = ActivationMap(size=1,dt=0.1,model='cnft',field=-1,th=0.75)
        self.uut.update(0.1)
        self.assertEqual(0,self.uut.getData())



if __name__ == '__main__':
    unittest.main()
