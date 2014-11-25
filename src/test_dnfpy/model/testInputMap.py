import numpy as np
import unittest
from dnfpy.model.inputMap import InputMap
import dnfpy.core.utils as utils
import os



class TestInputMap(unittest.TestCase):
    def setUp(self):
        self.gui = False
        if self.gui:
            import matplotlib.pyplot as plt
        self.precision = 7
        path =  os.path.dirname(os.path.realpath(__file__))
        self.testDir =path +  "/testFiles/"

        self.globalParams = \
                {'dt':0.1,'size':11,'wrap':True,'iStim':1,'wStim':2,'iDistr':1,'wDistr':2, \
                'nbDistr':2,'distr_dt':0.4,'tck_dt':0.2,'noise_dt':0.1,'noiseI':0., \
                'tck_radius':0.1,'input_dt':0.1}
        self.dt = 0.1

        self.uut = InputMap(self.globalParams['size'])
        self.uut.registerOnGlobalParamsChange_ignoreCompute(dt='input_dt',nb_distr='nbDistr')
        self.uut.updateParams(self.globalParams)

    def test_init(self):
        self.uut.update(0.1)
        self.assertEqual(0,np.sum(self.uut.getData()),"The noise is 0, the data should be 0")

    def test_updateTrack(self):
        self.uut.update(0.1)
        self.uut.update(0.2)
#       np.savetxt("TestInputMap02.csv",self.uut.getData(),delimiter=',')
        expected = np.around(np.loadtxt(self.testDir + "TestInputMap02.csv",delimiter=','),self.precision)
#        print("expeced %s"%expected)
        obtained = np.around(self.uut.getData(),self.precision)
#        print("obtained %s"%obtained)
        self.assertTrue((expected==obtained).all(),"the arrays should be the same")
        if self.gui:
            plt.imshow(obtained)
            plt.show()

    def test_updateDistr(self):
        self.uut.update(0.1)
        self.uut.update(0.2)
        self.uut.update(0.3)
        self.uut.update(0.4)
        obtained = np.around(self.uut.getData(),self.precision)
        if self.gui:
            plt.imshow(obtained)
            plt.show()




if __name__ == '__main__':
    unittest.main()
    