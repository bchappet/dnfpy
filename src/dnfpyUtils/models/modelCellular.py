from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.cellular.cellularMap import CellularMap
from getClassUtils import getFunctionFromName,getClassFromName

class ModelCellular(Model,Renderable):
    """
    The model is a subclass of CellularMap
    If model == None , the model will be CellularMap itself and a comp class needs to be provided

    Interface Comp:

    Return the new array
    +compute(data):


    Initialisa the first array:
    +initModel()

        

    By default comp is 'gameOfLife'

    """
    def initMaps(self,size,dim=2,dt=0.1,comp=None,model=None,**kwargs):

        if not(comp):
            comp = 'gameOfLife' 

        computationFunction = getFunctionFromName(comp, 'compute','cellular')

        if model:
            TheModel = getClassFromName(model,'cellular')
        else:
            TheModel = CellularMap

        self.map = TheModel("CellMap",size,dt=dt,dim=dim,computation=computationFunction,**kwargs)
        return self.map
    #override Renderable
    def getArrays(self):
        ret =  [self.map]
        ret.extend(self.map.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        self.map.onClick(x,y)
        return self.map

    def onRClick(self,mapName,x,y):
        self.map.onRClick(x,y)
        return self.map

