import math
from PyQt4 import QtGui
from PyQt4 import QtCore
import plotArrayQt
import numpy as np
from PyQt4.QtCore import pyqtSlot
class ArrayWidget(QtGui.QGroupBox):
    def __init__(self,map,runner,parametersView):
        super(ArrayWidget,self).__init__(title=map.getName())
        self.map = map
        self.runner = runner
        self.parametersView = parametersView
        self.label = ArrayLabel(self.title,map.getData(),runner,parametersView)
        self.label.setScaledContents(True)
        params = ArrayButtons(self)
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(params)
        self.paramsDisplayed = False

    def updateArray(self, array):
        self.label.updateArray(array.getData())
        if self.paramsDisplayed:
            pass
            #self.arrayParam.onMapUpdate()

    @pyqtSlot()
    def displayParams(self):
        if not (self.paramsDisplayed) :
            box = QtGui.QGroupBox(self.map.getName())
            self.paramsDisplayed = True
            #self.arrayParam = ArrayParams(self.map)
            self.paramDict = ParamsDict(self.map,self.runner)
            layout = QtGui.QVBoxLayout(box)
            #layout.addWidget(self.arrayParam)
            layout.addWidget(self.paramDict)

            self.parametersView.addWidget(box)


        else:
            #TODO Destroy
            pass

class ParamsDict(QtGui.QScrollArea):
    """
    Make a scrolable widget to display an set params dict
    """
    trigInt = QtCore.pyqtSignal(str,str,int)#Will be triggered on parmas modification
    trigFloat = QtCore.pyqtSignal(str,str,float)
    trigStr = QtCore.pyqtSignal(str,str,str)
    def __init__(self,map,runner):
        super(ParamsDict,self).__init__()
        self.map = map
        widget = QtGui.QWidget()
        layout = QtGui.QVBoxLayout(widget)

        self.trigInt.connect(runner.onParamIntChange)
        self.trigFloat.connect(runner.onParamFloatChange)
        self.trigStr.connect(runner.onParamStrChange)


        self.paramsList = []
        self.setWidgetResizable(True)

        for name in map.getAttributesNames():
            param = self.getParamWidg(name)
            self.connectToSlot(param)
            self.paramsList.append(param)
            layout.addWidget(param)

        self.setWidget(widget)


    def connectToSlot(self,widg):
        if isinstance(widg,QtGui.QSpinBox):
            widg.valueChanged.connect(self.onSpinIntValueChange)
        elif isinstance(widg,QtGui.QDoubleSpinBox):
            widg.valueChanged.connect(self.onSpinFloatValueChange)
        else:
            pass

    @pyqtSlot(str)
    def onSpinIntValueChange(self,val):
        name = self.sender().prefix()[:-2]
        self.trigInt.emit(self.map.getName(),name,val)

    @pyqtSlot(str)
    def onSpinFloatValueChange(self,val):
        name = self.sender().prefix()[:-2]
        self.trigFloat.emit(self.map.getName(),name,val)







    def getParamWidg(self,name):
        arg = self.map.getArg(name)

        if isinstance(arg,int):
            widg = QtGui.QSpinBox()
            if arg != 0:
                widg.setMaximum(100*arg)
            widg.setPrefix(name+": ")
            widg.setValue(arg)
        elif isinstance(arg,float):
            widg = QtGui.QDoubleSpinBox()
            if arg != 0:
                widg.setMaximum(100*arg)
            pointPrecision = (int(math.log10(arg))+1)
            if pointPrecision < 0:
                sst = 10.**(pointPrecision-1)
                widg.setSingleStep(sst)

            widg.setPrefix(name+": ")
            widg.setValue(arg)

        elif isinstance(arg,str):
            if arg in ('cnft','spike'):
                widg = QtGui.QComboBox()
                widg.addItem(arg)
                if arg == 'cnft':widg.addItem('spike')
                else: widg.addItem('cnft')
            else:
                print("unknow type of %s " % arg)
                widg = None

        else:
            print("unknow type of %s " % arg)
            widg = None
        if widg:
            widg.setMaximumWidth(120)

        return widg

    def onParamUpdate(self):
        for p in self.paramsList:
            name = p.getPrefix()[-2]
            p.setValue(self.map.getArg(name))







class ArrayParams(QtGui.QWidget):
    def __init__(self,map):
        super(ArrayParams,self).__init__(title=map.getName())
        self.map = map
        self.layout = QtGui.QVBoxLayout(self)
        self.lTime = QtGui.QLabel()
        self.lShape = QtGui.QLabel()
        self.layout.addWidget(self.lShape)
        self.layout.addWidget(self.lTime)

    def onMapUpdate(self):
        self.lTime.setText("Time: " + str(self.map.getArg('time')))
        self.lShape.setText("Shape: " + str(self.map.getData().shape))





class ArrayButtons(QtGui.QWidget):
    def __init__(self,arrayWidget):
        super(ArrayButtons,self).__init__()
        layout = QtGui.QHBoxLayout(self)
        bParams = QtGui.QPushButton("Infos")
        bParams.setMaximumHeight(30)
        layout.addWidget(bParams)
        self.setMaximumHeight(40)
        bParams.clicked.connect(arrayWidget.displayParams)



class ArrayLabel(QtGui.QLabel):
    triggerOnClick = QtCore.pyqtSignal(int,int)#Will be triggered on click
    def __init__(self,  name,  array, runner,parametersView):
        super(ArrayLabel,  self).__init__()
        self.name = name
        self.updateArray(array)
        self.runner = runner
        self.triggerOnClick.connect(runner.onClick)
        self.parametersView = parametersView

    def updateArray(self, array):
        self.array = array
        self.img = plotArrayQt.npToQImage(array)
        self.min = np.min(array)
        self.max = np.max(array)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.drawImage(event.rect(), self.img)
        qp.setPen(QtGui.QColor(0,0,0))
        qp.drawText(event.rect(),  QtCore.Qt.AlignTop,  "%.2f" %
                    self.max)
        qp.drawText(event.rect(),  QtCore.Qt.AlignBottom,  "%.2f" %
                    self.min)

    def mousePressEvent(self,  event):
        labXY = np.array([event.x(), event.y()], dtype=np.float32)
        size = self.rect().size()
        labWH = np.array([size.width(), size.height()]) - 1
        shapeWH = np.array([self.array.shape[0],
                            self.array.shape[1]]) - 1
        arrXY = (labXY / labWH) * shapeWH
        arrXY = np.round(arrXY)
        value = self.array[arrXY[1], arrXY[0]]
        print arrXY
        print value
        self.triggerOnClick.emit(arrXY[0],arrXY[1])



