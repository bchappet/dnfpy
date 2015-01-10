import unittest
import numpy as np
from dnfpy.cellular.bsRsdnfConvolution import BsRsdnfConvolution
from dnfpy.core.constantMap import ConstantMap
import dnfpy.view.staticViewMatplotlib as view


class TestBsRsdnfConvolutionMap(unittest.TestCase):
    def setUp(self):
        self.size = 101
        self.activation = np.zeros((self.size,self.size),np.intc)
        activationMap = ConstantMap("actmap",self.size, self.activation)
        self.uut = BsRsdnfConvolution("uut",self.size)
        self.uut.addChildren(activation=activationMap)

    def test_update(self):
        self.uut.compute()
        data = self.uut.getData()
        self.assertEqual(np.sum(data),0)


    def test_update_act(self):
        self.uut.setParamsRec(pSpike=0.01)
        self.uut.setParamsRec(sizeStream=100)
        self.uut.setParamsRec(pInh=0.1)
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                self.activation[self.size/2+i][self.size/2+j] = 1;
        self.uut.compute()
        self.activation = np.zeros((self.size,self.size),np.intc)
        for i in range(1000):
            self.uut.compute()
            print i
        data = self.uut.getData()
        print np.sum(data)
        view.plotArray(data)
        view.show()






if __name__ == "__main__":
    unittest.main()
