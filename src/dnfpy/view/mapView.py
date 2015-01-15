import sip
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot
from paramsView import ParamsView
from dnfpy.stats.clusterMap import ClusterMap
from dnfpy.stats.potentialTarget import PotentialTarget
from dnfpy.stats.trackedTarget import TrackedTarget
from dnfpy.stats.errorDist import ErrorDist
from arrayView import ArrayView
from clusterMapView import ClusterMapView
from potentialTargetView import PotentialTargetView
from trackedTargetView import TrackedTargetView
from errorDistView import ErrorDistView
class ArrayWidget(QtGui.QGroupBox):

    def __init__(self,map,runner,parametersView,view):
        super(ArrayWidget,self).__init__(title=map.getName())
        self.map = map
        self.view = view
        self.runner = runner
        self.parametersView = parametersView
        if isinstance(map,ClusterMap):
            self.label = ClusterMapView(self.map,runner,self)
        elif isinstance(map,PotentialTarget):
            self.label = PotentialTargetView(self.map,runner,self)
        elif isinstance(map,TrackedTarget):
            self.label = TrackedTargetView(self.map,runner,self)
        elif isinstance(map,ErrorDist):
            self.label = ErrorDistView(self.map,runner,self)
        else:
            self.label = ArrayView(self.map,runner,self)
        self.label.setScaledContents(True)
        params = ArrayButtons(self)
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(2,10,2,2)
        self.layout.addWidget(self.label)
        self.layout.addWidget(params)
        self.paramsDisplayed = False
        self.paramDict = None

    def updateArray(self):
        self.label.updateArray()
        if self.paramDict:
            self.paramDict.onMapUpdate()
    @pyqtSlot()
    def onParamsChanged(self):
        if self.paramDict:
            self.paramDict.onParamUpdate()


    @pyqtSlot()
    def displayParams(self):
        name = self.map.getName()
        if not (self.paramsDisplayed) :
            self.box = QtGui.QGroupBox(name)
            self.paramsDisplayed = True
            #self.arrayParam = ArrayParams(self.map)
            self.paramDict = ParamsView(self.map,self.runner,self.view)
            self.layoutB = QtGui.QVBoxLayout(self.box)
            #layout.addWidget(self.arrayParam)
            self.layoutB.addWidget(self.paramDict)

            self.parametersView.addWidget(name,self.box)
        else:
            self.paramsDisplayed = False
            sip.delete(self.paramDict)
            self.paramDict = None
            sip.delete(self.box)
            self.box = None

            self.parametersView.removeWidget(name)


class ArrayButtons(QtGui.QWidget):
    def __init__(self,arrayWidget):
        super(ArrayButtons,self).__init__()
        layout = QtGui.QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        bParams = QtGui.QPushButton("Infos")
        layout.addWidget(bParams)
        bParams.clicked.connect(arrayWidget.displayParams)




