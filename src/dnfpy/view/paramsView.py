import math
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import pyqtSlot

class ParamsView(QtGui.QScrollArea):
        """ 
            Generic class to get a map params view
            If you want a more dtailled view you should extend this class
        """
        trigInt = QtCore.pyqtSignal(str,str,int)#Will be triggered on parmas modification
        trigFloat = QtCore.pyqtSignal(str,str,float)
        trigStr = QtCore.pyqtSignal(str,str,str)
        trigAddChildren = QtCore.pyqtSignal(str)
        
        def __init__(self,map,runner,view):
                super(ParamsView,self).__init__()
                self.map = map
                widget = QtGui.QWidget()
                layout = QtGui.QVBoxLayout(widget)
                self.trigInt.connect(runner.onParamIntChange)
                self.trigFloat.connect(runner.onParamFloatChange)
                self.trigStr.connect(runner.onParamStrChange)
                self.trigAddChildren.connect(view.addChildrenMap)

                self.spinnerList = []
                self.labelList = []
                self.setWidgetResizable(True)

                for name in map.getAttributesNames():
                        param = self.getParamWidg(name)
                        self.connectToSlot(param)
                        layout.addWidget(param)
                for child in map.getChildren().values():
                        button = QtGui.QPushButton(child.getName())
                        button.clicked.connect(self.onChildrenButtonClicked)
                        layout.addWidget(button)
                self.setWidget(widget)

        def connectToSlot(self,widg):
                if isinstance(widg,QtGui.QSpinBox):
                    widg.valueChanged.connect(self.onSpinIntValueChange)
                elif isinstance(widg,QtGui.QDoubleSpinBox):
                    widg.valueChanged.connect(self.onSpinFloatValueChange)
                else:
                    #TODO string
                    pass

        @pyqtSlot()
        def onChildrenButtonClicked(self):
                name = self.sender().text()
                self.trigAddChildren.emit(name)

        @pyqtSlot(str)
        def onSpinIntValueChange(self,val):
                name = self.sender().prefix()[:-2]
                self.trigInt.emit(self.map.getName(),name,val)

        @pyqtSlot(str)
        def onSpinFloatValueChange(self,val):
                name = self.sender().prefix()[:-2]
                self.trigFloat.emit(self.map.getName(),name,val)


        def getStrParamWidg(self,arg,name):
                #TODO
                widg = QtGui.QComboBox()
                widg.addItem(arg)
                if arg == 'cnft':widg.addItem('spike')
                return None

        def specialWidgFloat(self,arg,name):
                if name[-1] == '_' or name in ['time']:
                    self.timeLabel = QtGui.QLabel(name+": "+str(arg))
                    return self.timeLabel
                else:
                    pass

        def getFloatParamWidg(self,arg,name):
                widg = self.specialWidgFloat(arg,name)
                if widg:
                        pass
                else:
                        widg = QtGui.QDoubleSpinBox()
                        if arg != 0:
                            widg.setMaximum(10000*arg)
                        pointPrecision = len(str(arg).split(".")[1])
                        #pointPrecision = (int(math.log10(arg))+1)
                        if pointPrecision > 0:
                            sst = 10.**(-pointPrecision)
                            widg.setSingleStep(sst)

                        widg.setPrefix(name+": ")
                        widg.setValue(arg)
                        self.spinnerList.append(widg)
                return widg

        def specialWidgInt(self,arg,name):
                if name[-1] == '_' or name in ['size'] :
                    widg = QtGui.QLabel(name+": "+str(arg))
                    self.labelList.append(widg)
                    return widg
                else:
                    pass


        def getIntParamWidg(self,arg,name):
                widg = self.specialWidgInt(arg,name)
                if widg:
                        pass
                else:
                        widg = QtGui.QSpinBox()
                        widg.setMaximum(10000)
                        widg.setMinimum(-10000)

                        widg.setPrefix(name+": ")
                        widg.setValue(arg)
                        self.spinnerList.append(widg)
                return widg


        def getParamWidg(self,name):
                arg = self.map.getArg(name)
                if isinstance(arg,int):
                    widg = self.getIntParamWidg(arg,name)
                elif isinstance(arg,float):
                    widg = self.getFloatParamWidg(arg,name)
                elif isinstance(arg,str):
                    widg = self.getStrParamWidg(arg,name)
                else:
                    print("unknow type of %s " % arg)
                    widg = None
                if widg:
                    widg.setMaximumWidth(140)
                return widg
        def onMapUpdate(self):
                self.timeLabel.setText("time: " + str(self.map.getArg('time')))

        def onParamUpdate(self):
                for p in self.spinnerList:
                    name = unicode(p.prefix())[:-2]
                    p.setValue(self.map.getArg(unicode(name)))
                for p in self.labelList:
                    name = unicode(p.text().split(": ")[0])
                    p.setText(name + ": " +unicode(self.map.getArg(name)))





