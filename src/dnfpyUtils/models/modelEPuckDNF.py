from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpyUtils.robots.VRep.vRepSimulator import VRepSimulator
from dnfpyUtils.robots.getIRSensors import GetIRSensors
from dnfpyUtils.robots.getDirection import GetDirection
from dnfpyUtils.robots.moteurProjection import MotorProjection
from dnfpy.model.mapDNF1D import MapDNFND
from dnfpy.model.convolutionND import ConvolutionND
from dnfpy.core.funcMapND import FuncMapND
import dnfpy.core.utilsND as utils

class ModelEPuckDNF(Model,Renderable):
    def initMaps(self, size
                 ):
        """We initiate the map and link them"""
        dt=0.1
        nbD = 20
        nbI = 20
        center = (size - 1)/2
        wrap=True
        #Create maps
        self.simulator = VRepSimulator("simulator",1,dt, synchronous=True)
                            
        self.simulator.connection()
        
        self.motorL = MotorProjection("motorL", 2, dt, 'l')
        self.motorR = MotorProjection("motorR", 2, dt, 'r')
        self.dnfmapI = MapDNFND("dnfmapI", size, dt=0.1, gainAff=100,tau=0.1, wInh=0.15, wrap=wrap)
        self.dnfmapD = MapDNFND("dnfmapD", size, dt=0.1, gainAff=10,tau=0.1, wrap=wrap)
        self.activationI = self.dnfmapI.getActivation()
        self.activationD = self.dnfmapD.getActivation()
        self.navigationMap = MapDNFND("navigationMap", size, dt, iExc=3.5, wInh=1.0, tau=0.3)
        self.navAff = FuncMapND(utils.subArrays, "navAff", size, dt=dt)
        
        
        self.modelI =ConvolutionND("IRSensorsModel",size,dt=dt,wrap=wrap)
        self.modelD =ConvolutionND("DirectionModel",size,dt=dt,wrap=wrap)
        self.kernel = FuncMapND(utils.gaussNd,"sensor_noseK",size,dt=dt,center=center,wrap=wrap,intensity=1,width=0.05*size)
        
        self.getIRSensors = GetIRSensors("IRSensors", size, dt, nbSensors=4)
        self.getDirection = GetDirection("Direction",size, dt)
        
        self.navigationMap.addChildren(aff=self.navAff)
        self.navAff.addChildren(a=self.activationD, b=self.activationI)
        self.modelI.addChildren(source=self.getIRSensors, kernel=self.kernel)
        self.modelD.addChildren(source=self.getDirection, kernel=self.kernel)
        self.motorL.addChildren(activationI=self.navigationMap.getActivation(), activationD = self.activationD, simulator=self.simulator)
        self.motorR.addChildren(activationI=self.navigationMap.getActivation(), activationD = self.activationD, simulator=self.simulator)
        self.activationI.addChildren(dnfmapI=self.dnfmapI)
        self.activationD.addChildren(dnfmapD=self.dnfmapD)
        self.getIRSensors.addChildren(simulator=self.simulator)
        self.getDirection.addChildren(simulator=self.simulator)
        self.dnfmapI.addChildren(aff=self.modelI)
        self.dnfmapD.addChildren(aff=self.modelD)
        #return the roots
        roots =  [self.motorL, self.motorR]

        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.motorL, self.motorR, self.activationI, self.dnfmapI, self.modelI, self.activationD, self.dnfmapD,  self.modelD, self.kernel, self.navigationMap, self.navigationMap.getActivation()]

        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
        
    def _reset(self):
        super(ModelEPuckDNF,self)._reset(
        )
        self.simulator.disconnection()
        self.simulator.connection()
        
