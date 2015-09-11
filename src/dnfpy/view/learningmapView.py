from PyQt4 import QtGui
from PyQt4 import QtCore
import numpy as np
import dnfpy.view.plotArrayQt

class ArrayWeightsView(QtGui.QLabel):
    def __init__(self,learningMap,coords):
        super(ArrayWeightsView,self).__init__()
        #self.setScaledContents(True)
        self.map = learningMap
        self.coords = coords
        self.img = None


    def reset(self):
        pass

    def updateArray(self):
        if self.coords in self.map.indicesActivated:
            self.array = self.map.getData()[self.coords[0],self.coords[1]]
            self.min = np.min(self.array)
            self.max = np.max(self.array)
            self.img = plotArrayQt.npToQImage(self.array)

    def paintEvent(self, event):
        if self.img:
            qp = QtGui.QPainter(self)
            qp.drawImage(event.rect(), self.img)

class LearningMapView(QtGui.QGraphicsView):
    triggerOnClick = QtCore.pyqtSignal(str,int,int)#Will be triggered on click
    triggerOnParamChanged = QtCore.pyqtSignal()
    #map name coord x y
    def __init__(self,  map, runner,mapView):
        super(LearningMapView,  self).__init__()
        self.map = map
        self.arrayLabels = [] #save the grid widgets
        self.updateArray()
        self.runner = runner
        self.triggerOnClick.connect(runner.onClick)
        self.triggerOnParamChanged.connect(mapView.onParamsChanged)

        self.initGridArray()
        self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag);

    def initGridArray(self):

        scene = QtGui.QGraphicsScene(self)
        self.setScene(scene)

        layout = QtGui.QGridLayout()
        layout.setHorizontalSpacing(1)
        layout.setVerticalSpacing(1)

        size = self.map.getArg('size')
        (height,width) = (size,size)
        for row in range(height):
            for col in range(width):
                label = (ArrayWeightsView(self.map,[row,col]))
                self.arrayLabels.append(label)
                layout.addWidget(label,row,col)

        viewWidget = QtGui.QWidget()
        viewWidget.setLayout(layout)
        layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        scene.addWidget(viewWidget)
        #selfLayout = QtGui.QVBoxLayout(self)
        #selfLayout.addWidget(viewWidget)

    def wheelEvent(self,event):
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse);
        #Scale the view / do the zoom
        scaleFactor = 1.15;
        if(event.delta() > 0) :
        # Zoom in
            self.scale(scaleFactor, scaleFactor);
        else :
        # Zooming out
            self.scale(1.0 / scaleFactor, 1.0 / scaleFactor);


    def reset(self):
        for label in self.arrayLabels:
            label.reset()

    def updateArray(self):
        for label in self.arrayLabels:
            label.updateArray()
