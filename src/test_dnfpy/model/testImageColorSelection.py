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
        self.uut = ImageColorSelection(size = self.img.shape[0],image = self.img)
        self.uut.registerOnGlobalParamsChange(dt='dt',color='color',reverseColors='reverseColors',color_threshold='color_threshold')
        self.params = dict(dt=0.1,color='red',reverseColors=False,color_threshold=20) 
        self.uut.updateParams(self.params)
    def test_red(self):
        self.params.update(color = 'red')
        self.uut.updateParams(self.params)
        self.uut.artificialRecursiveComputation()
        show2Img(self.img,self.uut.getData())
    def test_gray(self):
        self.params.update(color = 'gray')
        self.uut.updateParams(self.params)
        self.uut.artificialRecursiveComputation()
        show2Img(self.img,self.uut.getData())
        
if __name__ == "__main__":
    unittest.main()

        
