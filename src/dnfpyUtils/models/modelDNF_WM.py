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
                             iExc=2.2,iInh=1.5,
                             wExc=0.12/2.,wInh=0.26/2.,h=-0.2)
        #WM
        self.wm = ReceptiveFieldMap("WM",size,intensity=2.4,width=0.1)
        self.aff_WM = FuncWithoutKeywords(utils.weightedSumArrays,"WM_afferent",size)
        self.aff_WM.addChildren(
            ConstantMap("fFEF",1,value=1),
            self.fef.getActivation())
        self.wm.addChildren(source=self.aff_WM)
        self.wm_act = ActivationMap("WM_act",size,model=model)
        self.wm_act.addChildren(field=self.wm)

        #WM -> FEF
        self.WM_FEF = ReceptiveFieldMap("WM->FEF",size,intensity=2.1,width=0.08)
        self.WM_FEF.addChildren(source=self.wm_act)

        #DNF_ACT -> aff_FEF
        self.DNF_FEF = ReceptiveFieldMap("DNF->FEF",size,intensity=1.,width=0.1)
        self.DNF_FEF.addChildren(source=self.field.getActivation())

        #AFF of FEF : sum Input + Focus + WM
        self.aff_FEF = FuncWithoutKeywords(utils.weightedSumArrays,"FEF_afferent",size)
        fa = ConstantMap("fInput",1,value=1.)
        fb = ConstantMap("fDNF_FEF",1,value=1.)
        fc = ConstantMap("fWM",1,value=1.)
        self.aff_FEF.addChildren(fa,self.input,
                                 fb,self.DNF_FEF,
                                 fc,self.WM_FEF)

        self.fef.addChildren(aff=self.aff_FEF)

        #stats
        self.stats = StatsList(size,self.input,self.field.getActivation())
        #return the roots
        roots =  [self.fef.getActivation()]
        roots.extend(self.stats.getRoots())
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.input,self.field,self.field.getActivation(),
                self.DNF_FEF,self.aff_FEF,self.fef,self.fef.getActivation(),
                self.wm,self.wm_act,self.WM_FEF]

        #ret.extend(self.stats.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
