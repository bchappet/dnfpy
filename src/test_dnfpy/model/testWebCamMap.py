import unittest
from dnfpy.model.webcamMap import WebcamMap
import dnfpy.view.staticViewMatplotlib as view
import matplotlib.pyplot as plt
import cv2



class TestWebcamMap(unittest.TestCase):
        def test_cam1(self):
                uut = WebcamMap(512)
                uut.artificialRecursiveComputation()
                #view.plotArray(uut.getData())
                #plt.show()
#        def test_cam100(self):
#                uut = WebcamMap(512)
#                for i in range(100):
#                    uut.artificialRecursiveComputation()
#                view.plotArray(uut.getData())
#                plt.show()
#                plt.imsave("image2.png")



if __name__ == "__main__":
        unittest.main()

