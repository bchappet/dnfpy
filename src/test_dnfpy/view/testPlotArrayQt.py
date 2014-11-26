import unittest
from PyQt4 import  QtCore,QtGui
import plotArrayQt as uut
import sampleArrayGenerator as gen
import sys
import time


class testThread(QtCore.QThread):
    def __init__(self):
        super(testThread,self).__init__()
        self.app = QtGui.QApplication(sys.argv)
        self.app.exec_()

    def displayQImg(self,qimg):
        label = QtGui.QLabel()
        pixmap  = QtGui.QPixmap(qimg)
        label.setPixmap(pixmap)
        label.show()
    def stop(self):
        self.app.exit()

    
    
test = testThread()


class TestPlotArrayQt(unittest.TestCase):
        def setUp(self):
                self.size = 100
        def test_gradient_small_to_high(self):
                array = gen.getGradient(self.size,True)
                qimg = uut.npToQImage(array)
                test.displayQImg(qimg)
        def test_gradient_reversed(self):
                array = gen.getGradient(self.size,False)
                qimg = uut.npToQImage(array)
                test.displayQImg(qimg)

        @classmethod
        def tearDownClass(cls):
            testThread.stop()


if __name__ == '__main__':
    test.run()
    unittest.main()

                

