from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNF import MapDNF
from dnfpy.stats.statsList import StatsList
from dnfpyUtils.models.modelDNF import ModelDNF

class ModelDNFLin(ModelDNF):
    def initMaps(self,size=49,model="spike",activation="step",nbStep=0,
                 alphaExc=0.52,alphaInh=1.04,betaExc=3.53,betaInh=1.49,
                 alpha=10.,th=0.75,h=0
                 ):
        return super(ModelDNFLin,self).initMaps(size,model,activation,nbStep,
                        iExc=betaExc,iInh=betaInh,wExc=alphaExc,wInh=alphaInh,
                        lateral='dol',h=h,alpha=alpha,th=th)
