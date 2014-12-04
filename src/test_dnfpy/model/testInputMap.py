import numpy as np
import unittest
from dnfpy.model.inputMap import InputMap
import dnfpy.core.utils as utils
import os
import matplotlib.pyplot as plt




class TestInputMap(unittest.TestCase):
    def setUp(self):
        self.gui = False
        self.precision = 7

        self.globalParams = \
                {'dt':0.1,'size':21,'wrap':True,'iStim':1.,'wStim':0.1,'iDistr':1,
                 'wDistr':0.1,
                'nbDistr':0,'distr_dt':0.4,'tck_dt':0.2,'noise_dt':0.1,'noiseI':0., \
                'tck_radius':0.3,'input_dt':0.1}
        self.uut = InputMap(**self.globalParams)

    def test_init(self):
        self.uut.update(0.1)
        self.assertEqual(0,np.sum(self.uut.getData()))

    def test_updateTrack(self):
        self.uut.update(0.1)
        self.uut.update(0.2)
        plt.imshow(self.uut.getChildren()['track1'].getData())
        plt.show()

        #s/\n/,\r/g
        #s/\(\d\)\s\s\s/\1,/g
        expected = [
                   1.69572863e-11,4.87738516e-09,5.66367476e-07,2.65517192e-05,
                   5.02537878e-04,3.83996102e-03,1.18458783e-02,1.47533203e-02,
                   7.41818175e-03,1.50993012e-03,2.46819836e-04,1.50993234e-03,
                   7.41818920e-03,1.47533268e-02,1.18458839e-02,3.83996288e-03,
                   5.02537878e-04,2.65517301e-05,5.66375775e-07,4.88003504e-09,
                   1.73002411e-11]
        obtained = np.diagonal(self.uut.getData())
        self.assertAlmostEqual(0,np.sum(expected-obtained),self.precision)
    def test_updateTrack10(self):
        for time in np.arange(0,2,0.1):
                self.uut.update(time)
        #s/\n/,\r/g
        #s/\(\d\)\s\s\s/\1,/g
        expected = [
                1.07390772e-08,1.62045319e-06,9.87158855e-05,2.42784224e-03,
   2.41065733e-02,9.66345966e-02,1.56391054e-01,1.02181718e-01,
   2.69536078e-02,2.87254201e-03,2.46819487e-04,2.87253922e-03,
   2.69535836e-02,1.02181666e-01,1.56390980e-01,9.66345742e-02,
   2.41065789e-02,2.42784224e-03,9.87159801e-05,1.62045319e-06,
   1.07678311e-08]

        obtained = np.diagonal(self.uut.getData())
        self.assertAlmostEqual(0,np.sum(expected-obtained),self.precision)

    def test_updateDistr(self):
        self.uut.update(0.1)
        self.uut.update(0.2)
        self.uut.update(0.3)
        self.uut.update(0.4)
        obtained = np.around(self.uut.getData(),self.precision)

    def test_updateNbDistr(self):
        self.uut.update(0.1)
        self.uut.update(0.2)
        self.assertEqual(0,self.uut.get_nbDistr())
        self.uut.setArgRec(nbDistr=10)
        self.assertEqual(10,self.uut.get_nbDistr())
        self.uut.update(0.3)
        self.uut.update(0.4)
        self.uut.setArgRec(nbDistr=1)
        self.assertEqual(1,self.uut.get_nbDistr())



    def test_updateDistr(self):
        self.uut.update(0.1)
        self.uut.update(0.2)
        self.uut.update(0.3)
        self.uut.update(0.4)
        obtained = np.around(self.uut.getData(),self.precision)




if __name__ == '__main__':
    unittest.main()

