from dnfpy.core.funcMapND import FuncMapND
from dnfpy.core.funcWithoutKeywordsND import FuncWithoutKeywords
import dnfpy.core.utilsND as utils
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNFND import MapDNFND

class ModelDNF_WM(Model,Renderable):
    """
    28/04/2016
    Benoit Chappet de Vangel
    The ambition is to make a sequential scene exploration with two DNF maps

    Maps :
        field : dnf for the focus it will choose a target from the input
        wm : dnf to save the previously focused stimuli it will inhibit the field in return
        to force the focus on another stimulu

    """
    def initMaps(self,size=49,model="cnft",activation="step",nbStep=0,dim=2,wrap=True,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10.,alpha=10.,
                 iExc_wm=1.25,iInh_wm=0.7,wExc_wm=0.1,wInh_wm=10.,
                 wFocus=0.5,wInput=0.5,wAffInh = 1.0,
                 th=0.75,h=0,lateral='dog',
                 dt=0.1,**kwargs
                 ):
        """
        Main parameters are for the neural field (focus)
        _wm extension are for the Working Memory
        wFocus : weight of focus in afferent WM
        wInput : weight of input in afferent WM
        wAffInh : weight of inhibitino in return from WM to focus
        """
        self.field = MapDNFND("",size,dt=dt,dim=dim,model=model,activation=activation,nbStep=nbStep, \
                        iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh,th=th,h=h,lateral=lateral,wrap=wrap,wAffInh=wAffInh)
        self.wm    = MapDNFND("wm",size,dt=dt,dim=dim,model=model,activation=activation,nbStep=nbStep, \
                        iExc=iExc_wm,iInh=iInh_wm,wExc=wExc_wm,wInh=wInh_wm,th=th,h=h,lateral=lateral,wrap=wrap)

        self.afferentWM = FuncWithoutKeywords(utils.weightedSumArrays,'focus+input',size,dim=dim,dt=dt,paramList=['wFocus','wInput'],wFocus=wFocus,wInput=wInput)
        self.afferentWM.addChildren(self.field.act) #we will add input map later

        self.field.addChildren(afferentInhibition=self.wm.act)
        self.wm.addChildren(aff=self.afferentWM)



        
        #return the roots
        roots =  [self.field]
        return roots

    def onAfferentMapChange(self,afferentMap):
        self.field.addChildren(aff=afferentMap)
        self.afferentWM.addChildren(afferentMap)

    #override Renderable
    def getArrays(self):
        ret =  [self.field,self.field.act,self.afferentWM,self.wm,self.wm.act]
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%((mapName),x,y))
