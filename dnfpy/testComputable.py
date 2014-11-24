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

    def _compute(self,a,b,c,time):
        self.data = a +b *c + time
    def getArg(self,key):
        return self._getArg(key)
    def rmArg(self,key):
        return self._rmArg(key)

    def getArgs(self,*keys):
        return self._getArgs(keys)
    def getDictionaryNames(self):
        return self._getDictionaryNames()
    def subDictionary(self,keys):
        return self._subDictionary(keys)



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

    def test_getArg(self):
        obtained = self.uut.getArg('a')
        expected = 1
        self.assertEqual(expected,obtained,"shoud be equal")
    def test_nb_computation(self):
        self.uut.updateData(0.0)
        self.uut.updateData(0.0)
        self.uut.updateData(0.0)
        expected = 3
        obtained = self.uut.nb_computation
        self.assertEqual(expected,obtained,"shoud be equal")
    def test_rm_arg(self):
        ret = self.uut.rmArg('a')
        self.assertTrue(ret,"The key should be present")
        ret = self.uut.rmArg('a')
        self.assertFalse(ret,"The key should not be present")
    def test_last_computation_args(self):
        self.uut.updateData(0.1)
        obtained = self.uut.last_computation_args
        expected = dict(a=1,b=2,c=3,time=0.1)
        self.assertEqual(expected,obtained,"shoud be equal")
    def test_getArgs(self):
        obtained = self.uut.getArgs('a','b')
        expected = dict(a=1,b=2)
        self.assertEqual(expected,obtained,"shoud be equal")
    def test_getArgs_keyError(self):
        with self.assertRaises(KeyError):
            obtained = self.uut.getArgs('d','b')
    def test_get_dictionary_names(self):
        obtained = self.uut.getDictionaryNames()
        expected = set(['a','b','c','time'])
        self.assertEqual(expected,obtained,"shoud be equal")
    def test_sub_dictionary(self):
        obtained = self.uut.subDictionary(set(['a','b']))
        expected = dict(a=1,b=2)
        self.assertEqual(expected,obtained,"shoud be equal")
        

if __name__ == '__main__':
    unittest.main()
        

