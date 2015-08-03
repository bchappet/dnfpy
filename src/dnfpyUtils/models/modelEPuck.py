from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpyUtils.robots.VRep.vRepSimulator import VRepSimulator
from dnfpyUtils.robots.getIRSensors import GetIRSensors
from dnfpyUtils.robots.obstacleAvoidanceBehaviour import ObstacleAvoidanceBehaviour

class ModelEPuck(Model,Renderable):
    def initMaps(self
                 ):
        """We initiate the map and link them"""
       
        #Create maps
        self.simulator = VRepSimulator("simulator",1,0.1)
                            
        
        self.obstacle = ObstacleAvoidanceBehaviour("obstacle", 1, 0.1)
        
        
        self.getIRSensors = GetIRSensors("IRSensors", 1, 0.1) 
        
        
        self.obstacle.addChildren(irSensors=self.getIRSensors, simulator=self.simulator)
        self.getIRSensors.addChildren(simulator=self.simulator)
        
        #return the roots
        roots =  [self.obstacle]

        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.aff,self.field]
        ret.extend(self.field.getArrays())
        ret.extend(self.stats.getArrays())
        ret.append(self.stats.errorShape)
        ret.append(self.stats.shapeMap)
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))