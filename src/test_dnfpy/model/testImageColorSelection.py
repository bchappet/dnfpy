import numpy as np
import unittest
from dnfpy.model.imageColorSelection import ImageColorSelection
import matplotlib.pyplot as plt
import cv2
import dnfpy.view.staticViewMatplotlib as view
import os

def show2Img(im1,im2):
    view.plotArrays(dict(im1=im1,im2=im2))
    plt.show()

class TestImageColorSelection(unittest.TestCase):
    def setUp(self):
        path =  os.path.dirname(os.path.realpath(__file__))
        self.testDir =path +  "/testFiles/"

        self.img = cv2.imread(self.testDir + "exampleFinger.png")
        self.uut = ImageColorSelection("uut",size = self.img.shape[0],
            image = self.img,dt=0.1,color='red',reverseColors=False,thresh=20,
            lowHSV=np.array([150,50,50]),highHSV  = np.array([20,255,255]))
    def test_red(self):
        self.uut.compute()
        show2Img(self.img,self.uut.getData())
    def test_gray(self):
        self.uut.setArg(color='gray')
        self.uut.compute()
        show2Img(self.img,self.uut.getData())

if __name__ == "__main__":
    unittest.main()
