from dnfpy.model.inputMap1D import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.cellular.mapDNFBsRsdnf import MapDNFBsRsdnf

class ModelBsRsdnf(Model,Renderable):
    def initMaps(self,size,dt=0.1,sizeStream=100,pSpike=0.1,routerType="uniformCell",
            precisionProba=31,reproductible=False,iExc=1.57,iInh=0.74,pExc=1.3e-5,pInh=0.9,
                 mapType="fast",shift=5,nbSharedBit=31,
                 model='spike',activation='step',
                 **kwargs):
        """We initiate the map and link them"""

        """
        Before Fitting
        1.5,0.9,0.0043,0.4
        After Fitting
        1.53,0.76,0.00045,0.44
        After better fit:
        1.51, 0.79, 0.0006, 0.42
        After fit for 25 activation sp=0.1
        (1.96, 0.93, 1.30e-05, 1.)
        After optimization ga
        (1.96, 0.93, 4.826123183649009e-05, 3.712402448960776)
        After optimisation pSpike = 0.05
        (1.5735619684700972,0.7466390972842809,1.3e-05,1.0)
        Using fast model GA pSpike = 0.1
        [4.029, 3.861, 0.242, 1.065]
        """
        #pSpike=0.1
        #sizeStream=100
        #(iExc,iInh,pExc,pInh) = (1.5735619684700972,0.7466390972842809,1.3e-05,1.0)
        print("iExc %s, iInh %s, pExc %s, pInh %s"%(iExc,iInh,pExc,pInh))
        print("precisionProba: %s"%(precisionProba))
        if mapType == "doublefast":
            print("double fast : nbSharedBit %s, shift %s"%(nbSharedBit,shift))

        #Create maps
        #WM
        #self.field = MapDNFBsRsdnf("DNF",size,dt=dt,sizeStream=100,iExc=0.9,pInh=0.02)
        if mapType == "slow":
            dtPropagation = dt/100  #dt/(sizeStream + 2*size)
        else:
            dtPropagation = dt;
        print("sizeStream %s, dtPropagation %s pSpike %s"%(sizeStream,dtPropagation,pSpike))
        self.field = MapDNFBsRsdnf("Potential",size,dt=dt,dtPropagation=dtPropagation,
                                    precisionProba=precisionProba,
                                    reproductible=reproductible,
                                   sizeStream=sizeStream,
                                   pSpike=pSpike,
                                   routerType=routerType,
                                   iExc = iExc,iInh=iInh,
                                   pExc=pExc,pInh=pInh,
                                   shift=shift,nbSharedBit=nbSharedBit,
                                   mapType=mapType,model=model,activation=activation,
                                   )
        #return the roots
        roots =  [self.field]
        return roots

    #override Model
    def onAfferentMapChange(self,afferentMap):
        self.field.addChildren(aff=afferentMap)

    #override Renderable
    def getArrays(self):
        ret =  [self.field]
        ret.extend(self.field.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
