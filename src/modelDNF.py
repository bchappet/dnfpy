from dnfpy.model.inputMap import InputMap
from dnfpy.model.fieldMap import FieldMap
from dnfpy.model.activationMap import ActivationMap
from dnfpy.model.lateralWeightsMap import LateralWeightsMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.convolution import Convolution


class MapDNF(FieldMap):
    def __init__(self,size,**kwargs):
        super(MapDNF,self).__init__(size=size,**kwargs)
        self.act = ActivationMap(size)
        self.lat =Convolution(size)
        self.kernel = LateralWeightsMap(size,size)
        self.act.addChildren(field=self)
        self.addChildren(lat=self.lat)
        self.lat.addChildren(source=self.act,kernel=self.kernel)
        self.kernel.compute()

    def getArraysDict(self):
        return dict(Activation=self.act.getData(),
                    LateralInteractions=self.lat.getData(),
                    Kernel=self.kernel.getData())



class ModelDNF(Model,Renderable):
    def initMaps(self,size):
        """We initiate the map and link them"""
        #Create maps
        self.aff = InputMap(size)
        self.field = MapDNF(size)
        self.field.addChildren(aff=self.aff)
        #return the root
        return self.field
    #override Renderable
    def getArraysDict(self):
        ret =  dict(aff=self.aff.getData(),field=self.field.getData())
        ret.update(self.field.getArraysDict())
        return ret
