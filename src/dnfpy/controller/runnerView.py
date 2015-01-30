from dnfpy.view.dynamicViewQt import DisplayModelQt
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from datetime import datetime
import time
from runner import Runner
import sys


class RunnerView(QtCore.QThread, Runner):

    """
        The runner is the controller of the model and the view
        See MVC pattern
        The runner update view and model
        The view reads the model


        Attribute:
            model : Model
            view : View
    """
    triggerUpdate = QtCore.pyqtSignal()
    triggerParamsUpdate = QtCore.pyqtSignal(str)

    def __init__(
            self,
            model,
            view,
            timeEnd=100000,
            timeRatio=0.3,
            scenario=None):
        super(RunnerView, self).__init__()
        self.model = model
        self.view = view
        self.timeEnd = timeEnd
        self.timeRatio = timeRatio
        self.triggerUpdate.connect(self.view.update)
        self.triggerParamsUpdate.connect(self.view.updateParams)
        # timing
        self.lastUpdateTime = datetime.now()
        self.simuTime = 0.
        self.lastSimuTime = 0.
        # Control
        self.play = True
        # scenario
        self.scenario = scenario

    def getTimeRatio(self):
        return self.timeRatio

    @pyqtSlot(str, str, int)
    def onParamIntChange(self, mapName, name, value):
        self.model.updateParam(mapName, name, value)

    @pyqtSlot(str, str, float)
    def onParamFloatChange(self, mapName, name, value):
        self.model.updateParam(mapName, name, value)

    @pyqtSlot(str)
    def onSpinIntValueChange(self, val):
        name = self.sender().prefix()[:-2]
        self.trigInt.emit(self.map.getName(), name, val)

    @pyqtSlot(str, str, str)
    def onParamStrChange(self, mapName, name, value):
        print(
            "On param in t change in \"%s\" :  %s = %s " %
            (mapName, name, value))
        self.model.updateParam(mapName, name, value)

    @pyqtSlot(str, int, int)
    def onClick(self, mapName, x, y):
        mapName = str(mapName)
        mapToUpdate = self.model.onClick(mapName, x, y)
        if mapToUpdate:
            self.triggerParamsUpdate.emit(mapToUpdate)

    @pyqtSlot()
    def saveFigSlot(self):
        import dnfpy.view.staticViewMatplotlib as mtpl
        import matplotlib.pyplot as plt
        dic = self.model.getArraysDict()
        for key in dic:
            mtpl.plotArray(dic[key])
            plt.savefig(key+".png", dpi=300)
            plt.close()

    @pyqtSlot()
    def saveArrSlot(self):
        import numpy as np
        dic = self.model.getArraysDict()
        for key in dic:
            np.savetxt(key+".csv", dic[key], delimiter=",")

    @pyqtSlot(float)
    def setTimeRatio(self, timeRatio):
        self.timeRatio = timeRatio

    @pyqtSlot()
    def playSlot(self):
        self.play = not(self.play)

    @pyqtSlot()
    def stepSlot(self):
        self.step()

    @pyqtSlot()
    def resetSlot(self):
        self.lastUpdateTime = datetime.now()
        self.simuTime = 0.
        self.lastSimuTime = 0.
        self.model.reset()

    @pyqtSlot()
    def resetParamsSlot(self):
        self.model.resetParams()

    @pyqtSlot()
    def onClose(self):
        if self.scenario:
            print self.scenario.finalize(self.model, self)

    def step(self):
        if self.simuTime == 0:
            self.model.firstComputation()
        nextTime = self.model.getSmallestNextUpdateTime()
        self.lastSimuTime = self.simuTime
        self.simuTime = nextTime
        if self.scenario:
            self.scenario.apply(self.model, self.simuTime, self)
        self.model.update(self.simuTime)
        self.triggerUpdate.emit()

    def run(self):
        while self.simuTime < self.timeEnd:
            while not(self.play):
                time.sleep(0.1)
            self.step()
            self.__slowDown()

    def __slowDown(self):
        """
            Slow down computation to ensure that
            simuTime = timeRatio * realTime
        """
        now = datetime.now()

        delta = now - self.lastUpdateTime
        deltaModel = self.simuTime - self.lastSimuTime
        timeIteration = self.timeRatio * deltaModel * 1e6
        if delta.microseconds < timeIteration:
            val = (timeIteration - delta.microseconds)/1e6
            time.sleep(val)
        self.lastUpdateTime = now


def launch(model, context, scenario, timeRatio):
    defaultQSS = "stylesheet/default.qss"
    app = QtGui.QApplication([""])
    app.setStyleSheet(open(defaultQSS, 'r').read())

    if context:
        context.apply(model)
    if scenario:
        scenario.applyContext(model)
    view = DisplayModelQt(model)
    runner = RunnerView(model, view, timeRatio=timeRatio, scenario=scenario)
    view.setRunner(runner)
    view.show()
    runner.start()
    sys.exit(app.exec_())
