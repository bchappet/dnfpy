import sys
import imp
from dnfpy.view.dynamicViewQt import DisplayModelQt
from dnfpy.controller.runner import Runner
from PyQt4 import QtGui


defaultQSS = "stylesheet/default.qss"

modelName = sys.argv[1]
moduleName = modelName[0].lower() + modelName[1:]
fp, pathname, description = imp.find_module(moduleName)
module = imp.load_module(moduleName, fp, pathname, description)
clazz = getattr(module,modelName)


timeEnd = sys.argv[2] # simulation end
size= eval(sys.argv[3])
if len(sys.argv) > 4:
    timeRatio= eval(sys.argv[4])
else:
    timeRatio = 0.3



app = QtGui.QApplication(sys.argv)
app.setStyleSheet(open(defaultQSS,'r').read())



model = clazz(size)
view = DisplayModelQt(model)
#view.showMaximized()
runner = Runner(model,view,timeEnd,timeRatio)
view.setRunner(runner)



view.show()
runner.start()
sys.exit(app.exec_())
