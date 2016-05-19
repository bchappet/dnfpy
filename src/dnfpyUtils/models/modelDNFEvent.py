from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNFND import MapDNFND
from dnfpy.model.mapDNF import MapDNF
from dnfpy.model.lateralConvolution import LateralConvolution

class ModelDNFEvent(Model,Renderable):
    """
    """
    def initMaps(self,size=49,model="event",activation="step",nbStep=0,dim=2,wrap=True,
                 iExc=1.25,iInh=0.9,wExc=0.1,wInh=10.,alpha=10.,th=0.75,h=0.0,lateral='dog',noiseI=0.01,
                 dt=0.1,tau=0.64,iAff=0.06,wAff=0.1,**kwargs
                 ):
        """We initiate the map and link them"""
        self.field = MapDNFND("",size,dt=dt,dim=dim,model=model,activation=activation,nbStep=nbStep, \
                        iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh,th=th,h=h,lateral=lateral,wrap=wrap,tau=tau)
        self.affFilter = LateralConvolution("affFilter",size,dt=dt,dim=dim,wrap=wrap,lateral=lateral,nbStep=nbStep,iExc = iAff,wExc=wAff) 
        self.field.addChildren(aff=self.affFilter)

        roots =  [self.field]
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.field,self.field.lat.kernel]
        ret.extend(self.field.getArrays())
        return ret

    #override Model
    def onAfferentMapChange(self,afferentMap):
        #should be an DVS input
        self.affFilter.addChildren(source=afferentMap)

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%((mapName),x,y))
