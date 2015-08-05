from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpyUtils.robots.VRep.vRepSimulator import VRepSimulator
from dnfpyUtils.robots.getIRSensors import GetIRSensors
from dnfpyUtils.robots.moteurProjection import MotorProjection
from dnfpy.model.mapDNF1D import MapDNFND

class ModelEPuckDNF(Model,Renderable):
    def initMaps(self, size
                 ):
        """We initiate the map and link them"""
       
        #Create maps
        self.simulator = VRepSimulator("simulator",1,0.1)
                            
        self.simulator.connection()
        
        self.motorL = MotorProjection("motorL", 2, 0.1, 'l')
        self.motorR = MotorProjection("motorR", 2, 0.1, 'r')
        self.dnfmap = MapDNFND("dnfmap", 6)
        self.activation = self.dnfmap.getActivation()
        
        self.getIRSensors = GetIRSensors("IRSensors", 6, 0.1) 
        
        
        self.motorL.addChildren(activation=self.activation, simulator=self.simulator)
        self.motorR.addChildren(activation=self.activation, simulator=self.simulator)
        self.activation.addChildren(dnfmap=self.dnfmap)
        self.getIRSensors.addChildren(simulator=self.simulator)
        self.dnfmap.addChildren(aff=self.getIRSensors)
        #return the roots
        roots =  [self.motorL, self.motorR]

        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.motorL, self.motorR, self.activation, self.dnfmap, self.getIRSensors]

        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))