from dnfpy.core.funcMapND import FuncMapND
from dnfpy.model.lateralConvolution import LateralConvolution
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
    def initMaps(self,size=49,model="cnft",activation="step",nbStep=0,dim=2,wrap=True,alpha=10.,
                 iExc = 0.23,iInh = 0.13,wExc=0.12,wInh=1.60,h=-0.02,tau=0.37,
                 iExc_wm=0.71,iInh_wm=0.28,wExc_wm=0.067,wInh_wm=0.22,h_wm=-0.15,tau_wm=0.27,
                 wFocus=1.3,wInput=0.3,wAffInh = 1.0,
                 th=0.75,lateral='dog',dt=0.1,**kwargs
                 ):
        """
        Main parameters are for the neural field (focus)
        _wm extension are for the Working Memory
        wFocus : weight of focus in afferent WM
        wInput : weight of input in afferent WM
        wAffInh : weight of inhibitino in return from WM to focus
        """
        self.field = MapDNFND("",size,dt=dt,dim=dim,model=model,activation=activation,nbStep=nbStep, \
                        iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh,th=th,h=h,tau=tau,lateral=lateral,wrap=wrap,wAffInh=wAffInh)
        self.wm    = MapDNFND("wm",size,dt=dt,dim=dim,model=model,activation=activation,nbStep=nbStep, \
                        iExc=iExc_wm,iInh=iInh_wm,wExc=wExc_wm,wInh=wInh_wm,th=th,h=h_wm,tau=tau_wm,lateral=lateral,wrap=wrap)

        self.filteredFocus = LateralConvolution("filterFocus",size,dt=dt,dim=dim,wrap=wrap,lateral=lateral,nbStep=nbStep,iExc = wFocus,wExc=0.1) 
        self.filteredFocus.addChildren(source=self.field.act)
        self.filteredInput = LateralConvolution("filterInput",size,dt=dt,dim=dim,wrap=wrap,lateral=lateral,nbStep=nbStep,iExc = wInput,wExc=0.1) 
        self.afferentWM = FuncWithoutKeywords(utils.sumArrays,'focus+input',size,dim=dim,dt=dt)
        self.afferentWM.addChildren(self.filteredFocus,self.filteredInput)

        #self.afferentWM = FuncWithoutKeywords(utils.weightedSumArrays,'focus+input',size,dim=dim,dt=dt,paramList=['wFocus','wInput'],wFocus=wFocus,wInput=wInput)
        #self.afferentWM.addChildren(self.field.act) #we will add input map later

        self.field.addChildren(afferentInhibition=self.wm.act)
        self.wm.addChildren(aff=self.afferentWM)



        
        #return the roots
        roots =  [self.field]
        return roots

    def onAfferentMapChange(self,afferentMap):
        self.field.addChildren(aff=afferentMap)
        #self.afferentWM.addChildren(afferentMap)
        self.filteredInput.addChildren(source=afferentMap)

    #override Renderable
    def getArrays(self):
        ret =  [self.field,self.field.act,self.field.lat.kernel,self.afferentWM,self.wm,self.wm.act,self.wm.lat.kernel]
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%((mapName),x,y))
