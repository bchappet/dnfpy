import unittest
import numpy as np
from dnfpy.cellular.nSpikeConvolution import NSpikeConvolution
from dnfpy.core.funcWithoutKeywords import FuncWithoutKeywords
import dnfpy.core.utils as utils
from dnfpy.core.constantMap import ConstantMap
import dnfpy.view.staticViewMatplotlib as view


class TestNSpikeConvolutionMap(unittest.TestCase):
    def setUp(self):
        self.size = 101
        self.activation = np.zeros((self.size,self.size),np.intc)
        activationMap = ConstantMap("actmap",self.size, self.activation)
        self.uut = NSpikeConvolution("uut",self.size)
        self.uut.addChildren(activation=activationMap)

    def test_update(self):
        self.uut.compute()
        data = self.uut.getData()
        self.assertEqual(np.sum(data),0)


    def test_update_act(self):
        self.activation[self.size/2,self.size/2] = 1
        self.uut.compute()
        data = self.uut.getData()
        print np.sum(data)
        view.plotArray(data)
        view.show()






if __name__ == "__main__":
    unittest.main()
