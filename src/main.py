import sys
from dnfpy.view.dynamicViewQt import DisplayModelQt
from dnfpy.controller.runner import Runner
from PyQt4 import QtGui
import parser
import modelDNF
import modelDNFCam
import modelFingerDetection
import modelWMCam



defaultQSS = "stylesheet/default.qss"

modelName = sys.argv[1]
moduleName = modelName[0].lower() + modelName[1:]
baz = sys.modules[moduleName]
clazz = getattr(baz,modelName)



context = sys.argv[2] #arguments of the model
timeEnd = sys.argv[3] # simulation end
size= eval(sys.argv[4])

params = eval(open(context,'r').read())


app = QtGui.QApplication(sys.argv)
app.setStyleSheet(open(defaultQSS,'r').read())



model = clazz(size)
view = DisplayModelQt(model)
#view.showMaximized()
runner = Runner(model,view,timeEnd,params)
view.setRunner(runner)



view.show()
runner.start()
sys.exit(app.exec_())






