from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpyUtils.robots.VRep.vRepSimulator import VRepSimulator
from dnfpyUtils.robots.getIRSensors import GetIRSensors
from dnfpyUtils.robots.getDirection import GetDirection
from dnfpyUtils.robots.moteurProjection import MotorProjection
from dnfpy.model.mapDNF1D import MapDNFND

class ModelEPuckDNF(Model,Renderable):
    def initMaps(self, size
                 ):
        """We initiate the map and link them"""
        dt=0.1
        nbD = 20
        #Create maps
        self.simulator = VRepSimulator("simulator",1,dt, synchronous=False)
                            
        self.simulator.connection()
        
        self.motorL = MotorProjection("motorL", 2, dt, 'l')
        self.motorR = MotorProjection("motorR", 2, dt, 'r')
        self.dnfmapI = MapDNFND("dnfmapI", 6, dt=0.1, gainAff=100,tau=0.1)
        self.dnfmapD = MapDNFND("dnfmapD", nbD, dt=0.1, gainAff=10,tau=0.1)
        self.activationI = self.dnfmapI.getActivation()
        self.activationD = self.dnfmapD.getActivation()
        
        self.getIRSensors = GetIRSensors("IRSensors", 6, dt)
        self.getDirection = GetDirection("Direction",nbD,dt)
        
        
        self.motorL.addChildren(activationI=self.activationI, activationD = self.activationD, simulator=self.simulator)
        self.motorR.addChildren(activationI=self.activationI, activationD = self.activationD, simulator=self.simulator)
        self.activationI.addChildren(dnfmapI=self.dnfmapI)
        self.activationD.addChildren(dnfmapD=self.dnfmapD)
        self.getIRSensors.addChildren(simulator=self.simulator)
        self.getDirection.addChildren(simulator=self.simulator)
        self.dnfmapI.addChildren(aff=self.getIRSensors)
        self.dnfmapD.addChildren(aff=self.getDirection)
        #return the roots
        roots =  [self.motorL, self.motorR]

        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.motorL, self.motorR, self.activationI, self.dnfmapI, self.activationD, self.dnfmapD, self.getIRSensors]

        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
        
    def _reset(self):
        super(ModelEPuckDNF,self)._reset(
        )
        self.simulator.disconnection()
        self.simulator.connection()
        