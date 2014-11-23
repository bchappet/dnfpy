import inspect
import unittest
from computable import Computable

class Computable2(Computable):
    def __init__(self,**kwargs):
        super(Computable2,self).__init__(**kwargs)
        self.data = 0 #a pure attribute is not accessible in compute args
        self._setArg(time=0.0) #define like that the attribute/param will be accessible in compute args

    def getData(self):
        return self.data

    def updateData(self,compTime):
        self._setArg(time=compTime) 
        self._compute_with_params()

    def compute(self,a,b,c,time):
        self.data = a +b *c + time

    def registerOnGlobalParamChange(self,globalParam):
        pass


class TestComputable(unittest.TestCase):
    def setUp(self):
        self.uut = Computable2(a=1,b=2,c=3)
    def test_init_args(self):
        self.uut.updateData(0.0)
        obtained = self.uut.getData()
        expected = 7
        self.assertEqual(expected,obtained,"shoud be equal")
    def test_change_param_inside(self):
        self.uut.updateData(0.1)
        obtained = self.uut.getData()
        expected = 7+0.1
        self.assertEqual(expected,obtained,"shoud be equal")
    def test_with_to_many_arguments(self):
        """We construct with one unused arg
        the compute should work because we
        filter the args
        """
        self.uut = Computable2(a=1,b=2,c=3,d=3)
        self.uut.updateData(0.0)
        obtained = self.uut.getData()
        expected = 7
        self.assertEqual(expected,obtained,"shoud be equal")



        

if __name__ == '__main__':
    unittest.main()
        

