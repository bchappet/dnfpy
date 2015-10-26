from dnfpy.model.activationMap import ActivationMap
from dnfpy.model.fieldMap import FieldMap
from dnfpy.model.lateralWeightsMap import LateralWeightsMap
from dnfpy.model.lateralWeightsMapExp import LateralWeightsMapExp
from dnfpy.model.lateralWeightsMapLin import LateralWeightsMapLin
from dnfpy.model.convolution import Convolution

class MapDNF(FieldMap):
    """
    Generic map to build a DNF

    model : 'cnft' or 'spike' is the model of neurone rate coded or Leaky integrate and fire
    neuron parameters are
    th : threshold of activation
    h : resting potential
    tau : time constant of the neuron

    activation : 'step', 'sigm' or 'id' activation function

    lateral: 'dog','doe','dol' difference of gaussian, difference of exponential or diferrence of linear function
    The lateral weights parameters  are 
    iExc , iInh intensity of excitatatory and inhibitory component
    wExc , wInh width of excitatory and inhibitory component
    nbStep : discretisation of values of the lateral weights

    """
    def __init__(self,name,size,dt=0.1,wrap=True,
                 tau=0.64,h=0,
                 model='cnft',th=0.75,delta=1.,activation='step',
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10,alpha=10,
                 mapSize=1.,nbStep=0,lateral='dog',
                 **kwargs):
        super(MapDNF,self).__init__(name,size,dt=dt,wrap=wrap,
                    tau=tau,h=h,delta=delta,
                    model=model,th=th,activation=activation,
                    **kwargs)

        self.act = ActivationMap("Activation",size,dt=dt,type=activation,th=th)
        self.lat =Convolution("Lateral",size,dt=dt,wrap=wrap)
        
        if lateral=='dog':
            self.kernel = LateralWeightsMap(name+"Kernel",mapSize=mapSize,
                                        globalSize=size,wrap=wrap,
                                        iExc=iExc,iInh=iInh,wExc=wExc,
                                        wInh=wInh,alpha=alpha,nbStep=nbStep)
        elif lateral=='doe':
            self.kernel = LateralWeightsMapExp(name+"Kernel",mapSize=mapSize,
                                        globalSize=size,wrap=wrap,
                                        iExc=iExc,iInh=iInh,pExc=wExc,
                                        pInh=wInh,alpha=alpha,nbStep=nbStep)
        elif lateral=='dol':
            self.kernel = LateralWeightsMapLin(name+"Kernel",mapSize=mapSize,
                                        globalSize=size,wrap=wrap,
                                        betaExc=iExc,betaInh=iInh,alphaExc=wExc,
                                        alphaInh=wInh,alpha=alpha,nbStep=nbStep)
        else:
            raise("Parameter lateral should be 'dog', 'doe' or 'dol'. %s invalid"%(lateral))
        self.act.addChildren(field=self)
        self.addChildren(lat=self.lat)
        self.lat.addChildren(source=self.act,kernel=self.kernel)

    def getActivation(self):
        return self.act

    def getArrays(self):
        return [
            self.act,
            self.lat,
        ]
