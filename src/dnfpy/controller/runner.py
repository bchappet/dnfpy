from PyQt4 import QtCore

class Runner(QtCore.QThread):
    """
        The runner is the controller of the model and the view
        See MVC pattern
        The runner update view and model
        The view reads the model


        Attribute:
            model : Model
            view : View
    """
    trigger = QtCore.pyqtSignal()
    def __init__(self,model,view,timeEnd):
        super(Runner,self).__init__()
        self.model = model
        self.view = view
        self.simuTime = 0
        self.timeEnd = timeEnd
        self.trigger.connect(self.view.update)


    def run(self):
        while self.simuTime < self.timeEnd:
            nextTime = self.model.getSmallestNextUpdateTime()
            self.simuTime = nextTime
            self.model.update(self.simuTime)
            self.trigger.emit()

