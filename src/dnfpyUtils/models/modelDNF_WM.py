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
    def initMaps(self,size=49,model="spike",activation="step",nbStep=0,dim=2,wrap=False,alpha=10.,
                 th=0.75,lateral='step',dt=0.1,
                 iExc = 0.23,iInh = 0.13,wExc=0.12,wInh=1.60,h=-0.02,tau=0.37,
                 iExc_wm=0.71,iInh_wm=0.28,wExc_wm=0.067,wInh_wm=0.22,h_wm=-0.15,tau_wm=0.27,
                 iInputFocus=0.2,wInputFocus=0.1,iWMFocus=0.2,wWMFocus=0.1,
                 iInputWM=0.2,wInputWM=0.1,iFocusWM=0.2,wFocusWM=0.1,
                 **kwargs):
        """
        Main parameters are for the neural field (focus)
        _wm extension are for the Working Memory
        """
        self.focus = MapDNFND("",size,dt=dt,dim=dim,model=model,activation=activation,nbStep=nbStep, \
                        iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh,th=th,h=h,tau=tau,lateral=lateral,wrap=wrap)
        self.inputFocus = LateralConvolution("input->focus",size,dt=dt,dim=dim,wrap=wrap,lateral=lateral,nbStep=nbStep,iExc = iInputFocus,wExc=wInputFocus) 
        self.wmFocus = LateralConvolution("wm->focus",size,dt=dt,dim=dim,wrap=wrap,lateral=lateral,nbStep=nbStep,iExc = 0.0,wExc=0.0,iInh =iWMFocus,wInh=wWMFocus)
        self.afferentFocus = FuncWithoutKeywords(utils.sumArrays,'WM+input',size,dim=dim,dt=dt)
        self.afferentFocus.addChildren(self.inputFocus,self.wmFocus)
        self.focus.addChildren(aff=self.afferentFocus)



        self.wm = MapDNFND("wm",size,dt=dt,dim=dim,model=model,activation=activation,nbStep=nbStep, \
           iExc=iExc_wm,iInh=iInh_wm,wExc=wExc_wm,wInh=wInh_wm,th=th,h=h_wm,tau=tau_wm,lateral=lateral,wrap=wrap)
        self.focusWM = LateralConvolution("focus->wm",size,dt=dt,dim=dim,wrap=wrap,lateral=lateral,nbStep=nbStep,iExc = iFocusWM,wExc=wFocusWM) 
        self.inputWM = LateralConvolution("input->wm",size,dt=dt,dim=dim,wrap=wrap,lateral=lateral,nbStep=nbStep,iExc = iInputWM,wExc=wInputWM) 
        self.afferentWM = FuncWithoutKeywords(utils.sumArrays,'focus+input',size,dim=dim,dt=dt)
        self.afferentWM.addChildren(self.focusWM,self.inputWM)
        self.wm.addChildren(aff=self.afferentWM)

        self.wmFocus.addChildren(source=self.wm.act)
        self.focusWM.addChildren(source=self.focus.act)



        
        #return the roots
        roots =  [self.focus]
        return roots

    def onAfferentMapChange(self,afferentMap):
        self.inputFocus.addChildren(source=afferentMap)
        self.inputWM.addChildren(source=afferentMap)

    #override Renderable
    def getArrays(self):
        ret =  [self.focus,self.focus.act,self.focus.lat.kernel,
                self.afferentWM,self.wm,self.wm.act,self.wm.lat.kernel,
                self.inputFocus.kernel,self.inputWM.kernel]
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%((mapName),x,y))
