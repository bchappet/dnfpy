import dnfpy.view.staticViewMatplotlib as staticViewMatplotlib
import sampleArrayGenerator
import unittest
import matplotlib.pyplot as plt
import numpy as np
import scipy

class TestStaticViewMatplotlib(unittest.TestCase):
    def setUp(self):
        self.size = 100
        self.dog  = sampleArrayGenerator.getDOG2D(self.size)
    def test_plotArray(self):
        staticViewMatplotlib.plotArray(self.dog)
        plt.show()
    def test_plotArrays2(self):
        g1 = sampleArrayGenerator.getGaussian2D(self.size,self.size/4.)
        staticViewMatplotlib.plotArrays(dict(dog=self.dog,gauss=g1))
        plt.show()
    def test_plotArrays3(self):
        g1 = sampleArrayGenerator.getGaussian2D(self.size,self.size/4.)
        g2 = sampleArrayGenerator.getGaussian2D(self.size,self.size/3.5)*0.2
        staticViewMatplotlib.plotArrays(dict(dog=self.dog,gauss=g1,gauss2=g2))
        plt.show()
    def test_plotArrayVoid(self):
        staticViewMatplotlib.plotArray(np.zeros((self.size,self.size)))
        plt.show()
    def test_greyMap(self):
        img = scipy.misc.lena()
        staticViewMatplotlib.plotArray(img)
        plt.show()



        



if __name__ == '__main__':
    unittest.main()


