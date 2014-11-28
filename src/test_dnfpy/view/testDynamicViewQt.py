import unittest
from PyQt4 import  QtCore,QtGui
import sampleArrayGenerator as gen
import sys
import time
import dnfpy.view.dynamicViewQt as view
from dnfpy.view.renderable import Renderable

class RenderableTest(Renderable):
    def __init__(self,nbMap):
            self.arrays = {}
            for i in range(nbMap):
                self.arrays.update({"test"+str(i):gen.getRandomMarquedArray(size)})


    def update(self):
            for name in self.arrays.keys():
                    self.arrays.update({name:gen.getRandomMarquedArray(size)})
    def getArraysDict(self):
            return self.arrays


class TestThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal() 
    def __init__(self,renderable,view):
        super(TestThread,self).__init__()
        self.view = view
        self.renderable = renderable
        self.trigger.connect(self.view.update)
       

    def run(self):
        for i in range(10000):
            self.renderable.update()
            self.trigger.emit()
            time.sleep(0.05)

size = 150
nbMap = 15
def main():
    defaultQSS = "../../stylesheet/default.qss"
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(open(defaultQSS,'r').read())


    renderable = RenderableTest(nbMap)
    view_ = view.DisplayMapsQt(renderable)
    thread = TestThread(renderable,view_)
    view_.show()
    thread.start()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()

                

