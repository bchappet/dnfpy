from dnfpy.view.dynamicViewQt import DisplayModelQt
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from datetime import datetime
import time
from runner import Runner
import sys
import time


class RunnerView(QtCore.QThread, Runner):

    """
        The runner is the controller of the model and the view
        See MVC pattern
        The runner update view and model
        The view reads the model


        Attribute:
            model: Model, instance of Model
            view: View, instance of View
            timeEnd: float, end of the simulation (in second, simulator time referential)
            timeRatio: float, time ratio between simulator time referential and real time -> realTime/simTime
            scenario: Scenario, instance of Scenario to apply
            record: bool, if true the record mode is activated. An image named record.png will be produced 
                with checked map and trace and at specified time step
    """
    triggerUpdate = QtCore.pyqtSignal()
    triggerParamsUpdate = QtCore.pyqtSignal(str)

    def __init__(
            self,
            model,
            view,
            timeEnd=100000,
            timeRatio=0.3,
            scenario=None,
            record=False):
        """
        model : Model class of
        """
        super(RunnerView, self).__init__()
        Runner.__init__(self,model,timeEnd,scenario)

        self.view = view
        self.timeRatio = timeRatio
        self.triggerUpdate.connect(self.view.update)
        self.triggerParamsUpdate.connect(self.view.updateParams)
        # Control
        self.play = False
        #view timing
        self.lastViewUpdate = time.time()
        self.maxFPS = 60.

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

    @pyqtSlot(str, int, int)
    def onRClick(self, mapName, x, y):
        mapName = str(mapName)
        mapToUpdate = self.model.onRClick(mapName, x, y)
        if mapToUpdate:
            self.triggerParamsUpdate.emit(mapToUpdate)


    @pyqtSlot()
    def saveFigSlot(self):
        self.saveFig()

    @pyqtSlot()
    def saveArrSlot(self):
        self.saveArr()

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
        Runner.resetSlot(self)
        self.lastViewUpdate = time.time()

    @pyqtSlot()
    def resetParamsSlot(self):
        self.model.resetParams()

    @pyqtSlot()
    def onClose(self):
        if self.scenario:
            print(self.scenario.finalize(self.model, self))

    def step(self):
        if self.simuTime == 0:
            self.model.firstComputation()
        nextTime = self.model.getSmallestNextUpdateTime()
        self.lastSimuTime = self.simuTime
        self.simuTime = nextTime
        if self.scenario:
            self.scenario.apply(self.model, self.simuTime, self)
        self.model.update(self.simuTime)
        self.viewUpdate()

    def viewUpdate(self):
        """Ensure that the view update frequency is not higher than maxFPS"""
        now = time.time()
        deltaTime = now -  self.lastViewUpdate
        limit = (1./self.maxFPS)
        if deltaTime >= limit:
            self.triggerUpdate.emit()
            self.lastViewUpdate = now

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


def launch(model, scenario, timeRatio, record=False):
    defaultQSS = "stylesheet/default.qss"
    app = QtGui.QApplication([""])
    app.setStyleSheet(open(defaultQSS, 'r').read())

    if scenario:
        scenario.applyContext(model)
    view = DisplayModelQt(model)
    runner = RunnerView(model, view, timeRatio=timeRatio, scenario=scenario, record=record)
    view.setRunner(runner)
    view.show()
    runner.start()
    sys.exit(app.exec_())