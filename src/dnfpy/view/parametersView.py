from PyQt4 import QtGui

class ParametersView(QtGui.QWidget):
    def __init__(self,runner):
        super(ParametersView,self).__init__()
        self.layout = QtGui.QVBoxLayout(self)

    def addWidget(self,widget):
        self.layout.addWidget(widget)

