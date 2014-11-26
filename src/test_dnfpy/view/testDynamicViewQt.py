import unittest
from PyQt4 import  QtCore,QtGui
import sampleArrayGenerator as gen
import sys
import time
import dnfpy.view.dynamicViewQt as view


class TestThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal() 
    def __init__(self,gui):
        super(TestThread,self).__init__()
        self.gui = gui
        self.trigger.connect(self.gui.update)
        for i in range(nbMap):
            gui.addMap(gen.getRandomMarquedArray(size))
       

    def run(self):
        for i in range(1000):
            for j in range(nbMap):
                self.gui.addMapToUpdate(j,gen.getRandomMarquedArray(size))
            self.trigger.emit()
            time.sleep(0.01)

    



size = 150
nbMap = 15
def main():
    app = QtGui.QApplication(sys.argv)
    ex = view.DisplayMapsQt(nbMap)
    thread = TestThread(ex)
    ex.show()
    thread.start()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()

                

