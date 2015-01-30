from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNF import MapDNF
from dnfpy.stats.statsList import StatsList
from dnfpy.model.receptiveFieldMap import ReceptiveFieldMap
from dnfpy.core.funcWithoutKeywords import FuncWithoutKeywords
import dnfpy.core.utils as utils
from dnfpy.core.constantMap import ConstantMap
from dnfpy.model.activationMap import ActivationMap

class ModelDNF_WM(Model,Renderable):
    def initMaps(self,size=49,model="spike",nbStep=0):
        """We initiate the map and link them"""
        #Create maps
        self.input = InputMap("Inputs",size)
        self.field = MapDNF("DNF",size,model=model,nbStep=nbStep)
        self.field.addChildren(aff=self.input)

        mapSize = 0.3
        #FEF
        self.fef = MapDNF("FEF",size,mapSize=mapSize,model=model,
                             iExc=2.0,iInh=1.2,
                             wExc=0.12/2.,wInh=0.28/2.,h=-0.2)
        #WM
        self.wm = ReceptiveFieldMap("FEF->WM",size,intensity=3.4,width=0.08)
        self.wm.addChildren(source=self.fef.getActivation())
        self.wm_act = ActivationMap("WM_act",size,model=model)
        self.wm_act.addChildren(field=self.wm)

        #WM -> FEF
        self.WM_FEF = ReceptiveFieldMap("WM->FEF",size,intensity=1.8,width=0.1)
        self.WM_FEF.addChildren(source=self.wm_act)

        #DNF_ACT -> FEF
        self.DNF_FEF = ReceptiveFieldMap("DNF->FEF",size,intensity=1.,width=0.1)
        self.DNF_FEF.addChildren(source=self.field.getActivation())

        #INPUT -> FEF
        self.INPUT_FEF = ReceptiveFieldMap("INPUT->FEF",size,intensity=0.3,width=0.1)
        self.INPUT_FEF.addChildren(source=self.input)

        #AFF of FEF : sum Input + Focus + WM
        self.aff_FEF = FuncWithoutKeywords(utils.sumArrays,"FEF_afferent",size)
        self.aff_FEF.addChildren(self.INPUT_FEF,
                                 self.DNF_FEF,
                                 self.WM_FEF)

        self.fef.addChildren(aff=self.aff_FEF)

        #stats
        self.stats = StatsList(size,self.input,self.fef.getActivation())
        #return the roots
        roots =  [self.fef.getActivation()]
        roots.extend(self.stats.getRoots())
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.INPUT_FEF,self.field,self.field.getActivation(),
                self.DNF_FEF,self.aff_FEF,self.fef,self.fef.getActivation(),
                self.wm,self.wm_act,self.WM_FEF]

        ret.extend(self.stats.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
