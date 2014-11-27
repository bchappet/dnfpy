import sys
from modelDNF import ModelDNF
from modelDNFCam import ModelDNFCam
from dnfpy.view.dynamicViewQt import DisplayMapsQt
from dnfpy.controller.runner import Runner
from PyQt4 import QtGui
import parser

modelName = sys.argv[1]
moduleName = modelName[0].lower() + modelName[1:]
baz = sys.modules[moduleName]
clazz = getattr(baz,modelName)



context = sys.argv[2] #arguments of the model
timeEnd = sys.argv[3] # simulation end

params = eval(open(context,'r').read()) 


app = QtGui.QApplication(sys.argv)
model = clazz(params)
view = DisplayMapsQt(model)
runner = Runner(model,view,timeEnd)


view.show()
runner.start()
sys.exit(app.exec_())






