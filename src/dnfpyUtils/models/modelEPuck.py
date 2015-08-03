from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpyUtils.robots.VRep.vRepSimulator import VRepSimulator
from dnfpyUtils.robots.getIRSensors import GetIRSensors
from dnfpyUtils.robots.obstacleAvoidanceBehaviour import ObstacleAvoidanceBehaviour

class ModelEPuck(Model,Renderable):
    def initMaps(self, size
                 ):
        """We initiate the map and link them"""
       
        #Create maps
        self.simulator = VRepSimulator("simulator",1,0.1)
                            
        self.simulator.connection()
        
        self.obstacle = ObstacleAvoidanceBehaviour("obstacle", 2, 0.1)
        
        
        self.getIRSensors = GetIRSensors("IRSensors", 8, 0.1) 
        
        
        self.obstacle.addChildren(irSensors=self.getIRSensors, simulator=self.simulator)
        self.getIRSensors.addChildren(simulator=self.simulator)
        
        #return the roots
        roots =  [self.obstacle]

        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.obstacle,self.getIRSensors]

        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))