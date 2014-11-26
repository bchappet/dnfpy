import sys
from modelDNF import ModelDNF
from dnfpy.view.dynamicViewQt import DisplayMapsQt
from dnfpy.controller.runner import Runner
from PyQt4 import QtGui

context = sys.argv[1] #arguments of the model
timeEnd = sys.argv[2] # simulation end

params = eval(open(context,'r').read()) 

app = QtGui.QApplication(sys.argv)
model = ModelDNF(params)
view = DisplayMapsQt(model)
runner = Runner(model,view,timeEnd)


view.show()
runner.start()
sys.exit(app.exec_())






