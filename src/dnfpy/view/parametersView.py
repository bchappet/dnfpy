from PyQt4 import QtGui

class ParametersView(QtGui.QWidget):
    def __init__(self,runner):
        super(ParametersView,self).__init__()
        self.layout = QtGui.QVBoxLayout(self)
	self.__nbWidg = 0
	self.setMaximumWidth(0)

    def addWidget(self,widget):
	if self.__nbWidg == 0:
		self.setMaximumWidth(300)
	self.__nbWidg =+ 1
        self.layout.addWidget(widget)

