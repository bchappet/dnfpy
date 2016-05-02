from dnfpy.core.funcMapND import FuncMapND
from dnfpy.model.lateralConvolution import LateralConvolution
from dnfpy.core.funcWithoutKeywordsND import FuncWithoutKeywords
import dnfpy.core.utilsND as utils
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNFND import MapDNFND

class ModelWM(Model,Renderable):
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
                 iExc_wm=0.08,iInh_wm=0.03,wExc_wm=0.16,wInh_wm=0.43,h_wm=-0.08,tau_wm=0.16,
                 iFocus=0.7,iInput=0.3,wFocus=0.1,wInput=0.1,
                 th=0.75,lateral='dog',dt=0.1,**kwargs
                 ):
        """
        Main parameters are for the neural field (focus)
        _wm extension are for the Working Memory
        wFocus : weight of focus in afferent WM
        wInput : weight of input in afferent WM
        wAffInh : weight of inhibitino in return from WM to focus
        """
        self.wm    = MapDNFND("",size,dt=dt,dim=dim,model=model,activation=activation,nbStep=nbStep, \
                        iExc=iExc_wm,iInh=iInh_wm,wExc=wExc_wm,wInh=wInh_wm,th=th,h=h_wm,tau=tau_wm,lateral=lateral,wrap=wrap)

        self.filteredFocus = LateralConvolution("filterFocus",size,dt=dt,dim=dim,wrap=wrap,lateral=lateral,nbStep=nbStep,iExc = iFocus,wExc=wFocus) 
        self.filteredInput = LateralConvolution("filterInput",size,dt=dt,dim=dim,wrap=wrap,lateral=lateral,nbStep=nbStep,iExc = iInput,wExc=wInput) 
        self.afferentWM = FuncWithoutKeywords(utils.sumArrays,'focus+input',size,dim=dim,dt=dt)
        self.afferentWM.addChildren(self.filteredFocus,self.filteredInput)
        self.wm.addChildren(aff=self.afferentWM)



        
        #return the roots
        roots =  [self.wm]
        return roots

    def onAfferentMapChange(self,afferentMap,focusMap):
        self.filteredInput.addChildren(source=afferentMap)
        self.filteredFocus.addChildren(source=focusMap)

    #override Renderable
    def getArrays(self):
        ret =  [self.afferentWM,self.wm,self.wm.act,self.wm.lat.kernel,
                self.filteredFocus,self.filteredInput]
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%((mapName),x,y))
