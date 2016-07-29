from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNFND import MapDNFND


class ModelDNF(Model,Renderable):
    """
    For DOG:
        {'iExc' : 1.25,'iInh' : 0.7,'wExc' : 0.1,'wInh': 0.9}
    For DOE:
        {'wExc' : 0.0043, 'wInh':0.9}
    For DOL:
        {'iExc' : 0.15,'iInh' : 0.65,'wExc' : 9.16, 'wInh' : 1.10}

    DOG spike
    {'model': 'spike', 'dim': 2, 'activation': 'step', 'iInh': 0.64538669980233787, 'tau': 0.12687111199574119, 'size': 49, 'lateral': 'dog', 'h': 0, 'wExc': 0.47008654993640697, 'iExc': 0.6584865701410707, 'dt': 0.1, 'wInh': 0.76977930800179117}

    """
    def initMaps(self,size=49,model="spike",activation="step",nbStep=0,dim=2,wrap=True,
                 #iExc=1.25,iInh=0.7,wExc=0.1,wInh=10.,alpha=10.,th=0.75,h=0.0,
                iInh =  0.64538669980233787, wExc= 0.47008654993640697, iExc= 0.6584865701410707,  wInh= 0.76977930800179117,tau=0.13,
                 
                 lateral='dog',noiseI=0.01,
                 dt=0.1,h=0,th=0.75,
                 sfa=False,tauSFA=1.0,mSFA=4.8,betaSFA=0.2,
                errorProb=0.0,errorType='none',

                 **kwargs
                 ):
        """We initiate the map and link them"""
        self.field = MapDNFND("",size,dt=dt,dim=dim,model=model,activation=activation,nbStep=nbStep, \
                        iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh,th=th,h=h,lateral=lateral,wrap=wrap,tau=tau,
                        sfa=sfa,tauSFA=tauSFA,mSFA=mSFA,beta=betaSFA,
                        errorProb=errorProb,errorType=errorType,
                        )
        #return the roots
        roots =  [self.field]
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.field,self.field.lat.kernel]
        ret.extend(self.field.getArrays())
        return ret

    #override Model
    def onAfferentMapChange(self,afferentMap):
        self.field.addChildren(aff=afferentMap)

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%((mapName),x,y))
