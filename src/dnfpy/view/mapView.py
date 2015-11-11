import sip
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot
from dnfpy.view.paramsView import ParamsView
from dnfpyUtils.stats.clusterMap import ClusterMap
from dnfpyUtils.stats.potentialTarget import PotentialTarget
from dnfpyUtils.stats.trackedTarget import TrackedTarget
from dnfpyUtils.stats.errorDist import ErrorDist
from dnfpyUtils.stats.errorDistSimple import ErrorDistSimple
from dnfpyUtils.stats.errorShape import ErrorShape
from dnfpy.view.arrayView import ArrayView
from dnfpy.view.arrayView2 import ArrayView2
from dnfpy.view.clusterMapView import ClusterMapView
from dnfpy.view.potentialTargetView import PotentialTargetView
from dnfpy.view.trackedTargetView import TrackedTargetView
from dnfpy.view.errorDistView import ErrorDistView
from dnfpy.view.learningmapView import LearningMapView
from dnfpy.view.multiLayerMapView import MultiLayerMapView
from dnfpy.view.multiLayerMapAliveView import MultiLayerMapAliveView
from dnfpy.learning.learningMap import STDPLearningMap
from dnfpy.model.multiLayerMap import MultiLayerMap
from dnfpy.model.multiLayerMapAlive import MultiLayerMapAlive
from dnfpy.core.mapND import MapND
from dnfpy.view.arrayNDView import ArrayNDView

from dnfpyUtils.cellular.fhp import Fhp

from dnfpy.view.fhpMapView import FhpMapView
from dnfpy.view.trajectoryView import TrajectoryView
from dnfpy.view.tupleView import TupleView


from dnfpy.view.multipleData import MultipleData
from dnfpy.view.multipleDataView import MultipleDataView
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
        elif isinstance(map,ErrorDist) or isinstance(map,ErrorDistSimple) or isinstance(map,ErrorShape):
            self.label = ErrorDistView(self.map,runner,self)
        elif isinstance(map,STDPLearningMap):
            self.label = LearningMapView(self.map,runner,self)
        elif isinstance(map,MultiLayerMapAlive):
            self.label = MultiLayerMapAliveView(self.map,runner,self)
        elif isinstance(map,MultiLayerMap):
            self.label = MultiLayerMapView(self.map,runner,self)
        elif isinstance(map,Fhp):
            self.label = FhpMapView(self.map,runner,self)
        elif isinstance(map,MultipleData):
            self.label = MultipleDataView(self.map,runner,self)
        elif isinstance(map,MapND):
            dim = map.getArg('dim')
            size = map.getArg('size')
            if size == 0 and dim == 0: #scalar
                self.label = TrajectoryView(self.map,runner,self)
            elif size == 0 and dim != 0:
                self.label = TupleView(self.map,runner,self) #it will be displayed as a dot on a ndim view with a nice trace
            elif dim == 1:
                self.label = ArrayNDView(self.map,runner,self)
            elif dim == 2:
                self.label = ArrayView(self.map,runner,self)
            else:
                raise Exception("No display for dimension ",dim)
        else:
            self.label = ArrayView(self.map,runner,self)
            #self.label = ArrayView2(self.map,runner,self)




        self.params = ArrayButtons(self)
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(2,10,2,2)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.params)
        self.paramsDisplayed = False
        self.paramDict = None


        if isinstance(self.label,QtGui.QLabel):
            self.label.setScaledContents(True)
        else:
            pass
            #self.setFixedSize(400,400)

    def updateArray(self):
        self.label.updateArray()
        if self.paramDict:
            self.paramDict.onMapUpdate()
    @pyqtSlot()
    def onParamsChanged(self):
        if self.paramDict:
            self.paramDict.onParamUpdate()

    def reset(self):
        self.label.reset()


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

    @pyqtSlot()
    def toggleView(self):
            self.label.toggleView()



class ArrayButtons(QtGui.QWidget):
    def __init__(self,arrayWidget):
        super(ArrayButtons,self).__init__()
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        bParams = QtGui.QPushButton("Infos")
        bToggleView = QtGui.QPushButton("Toggle View")
        self.layout.addWidget(bParams)
        self.layout.addWidget(bToggleView)
        bParams.clicked.connect(arrayWidget.displayParams)
        bToggleView.clicked.connect(arrayWidget.toggleView)

#       self.checkBox = QtGui.QCheckBox("save")
#       self.layout.addWidget(self.checkBox)




