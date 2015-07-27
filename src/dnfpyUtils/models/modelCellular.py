from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.cellular.cellularMap import CellularMap
from getClassUtils import getFunctionFromName,getClassFromName

class ModelCellular(Model,Renderable):
    def initMaps(self,size,comp=None,model=None,**kwargs):
        if comp:
            computationFunction = getFunctionFromName(comp, 'compute','cellular')
        else:
            computationFunction = None

        if model:
            TheModel = getClassFromName(model,'cellular')
        else:
            TheModel = CellularMap

        self.map = TheModel("CellMap",size,dt=0.1,computation=computationFunction,**kwargs)
        return self.map
    #override Renderable
    def getArrays(self):
        ret =  [self.map]
        ret.extend(self.map.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        self.map.onClick(x,y)
        return self.map.name

    def onRClick(self,mapName,x,y):
        self.map.onRClick(x,y)
        return self.map.name

