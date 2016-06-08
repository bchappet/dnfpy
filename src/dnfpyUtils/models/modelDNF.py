from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNFND import MapDNFND
from dnfpy.model.mapDNF import MapDNF

class ModelDNF(Model,Renderable):
    """
    For DOG:
        {'iExc' : 1.25,'iInh' : 0.7,'wExc' : 0.1,'wInh': 0.9}
    For DOE:
        {'wExc' : 0.0043, 'wInh':0.9}
    For DOL:
        {'iExc' : 0.15,'iInh' : 0.65,'wExc' : 9.16, 'wInh' : 1.10}



    """
    def initMaps(self,size=49,model="cnft",activation="step",nbStep=0,dim=2,wrap=True,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10.,alpha=10.,th=0.75,h=0.0,lateral='dog',noiseI=0.01,
                 dt=0.1,tau=0.64,
                 sfa=False,tauSFA=1.0,mSFA=4.8,betaSFA=0.2,
                 **kwargs
                 ):
        """We initiate the map and link them"""
        self.field = MapDNFND("",size,dt=dt,dim=dim,model=model,activation=activation,nbStep=nbStep, \
                        iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh,th=th,h=h,lateral=lateral,wrap=wrap,tau=tau,
                        sfa=sfa,tauSFA=tauSFA,mSFA=mSFA,beta=betaSFA,
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
