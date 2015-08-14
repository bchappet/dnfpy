from dnfpy.view.renderable import Renderable
import numpy as np
from dnfpy.model.model import Model
from dnfpyUtils.robots.VRep.vRepSimulator import VRepSimulator
from dnfpyUtils.robots.getIRSensors import GetIRSensors
from dnfpyUtils.robots.getDirection import GetDirection
from dnfpyUtils.robots.moteurProjection import MotorProjection
from dnfpy.model.mapDNF1D import MapDNFND
from dnfpy.model.convolutionND import ConvolutionND
from dnfpy.core.funcMapND import FuncMapND
import dnfpy.core.utilsND as utils
from dnfpy.core.constantMap import ConstantMap
from dnfpy.robots.robotSimulator import RobotSimulator
from dnfpy.core.gainMap import GainMap



class ModelEPuckDNF_test(Model,Renderable):
    def initMaps(self, size
                 ):
        """We initiate the map and link them"""
        dt=0.1
        nbD = 20
        nbI = 20
        center = (size - 1)/2
        wrap=True
        #Create maps
        self.simulator = RobotSimulator("simulator",1,dt, synchronous=True)
                            
        #self.simulator.connection()
        
        self.motorL = MotorProjection("motorL", 2, dt, 'l')
        self.motorR = MotorProjection("motorR", 2, dt, 'r')
        self.dnfmapI = MapDNFND("dnfmapI", size, dt=0.1, gainAff=1,tau=1, wInh=0.15, wrap=wrap,activation='sigm')
        self.dnfmapD = MapDNFND("dnfmapD", size, dt=0.1, gainAff=1,tau=0.1, wrap=wrap)
        self.activationI = GainMap(self.dnfmapI.getActivation(),gain=1.0)
        self.activationD = GainMap(self.dnfmapD.getActivation(),gain=2.0)
        self.navigationMap = MapDNFND("navigationMap", size, dt,gainAff=2.0, iExc=1.6,wExc=0.07,iInh=0.3, wInh=1.0, tau=0.3,h=-0.5,activation='sigm')
        self.navAff = FuncMapND(utils.subArrays, "navAff", size, dt=dt)
        self.navAffGain = GainMap(self.navAff,gain=0.5)
        
        
        self.modelI =ConvolutionND("IRSensorsModel",size,dt=dt,wrap=wrap)
        self.modelD =ConvolutionND("DirectionModel",size,dt=dt,wrap=wrap)
        self.kernelI = FuncMapND(utils.gaussNd,"I_noiseK",size,dt=dt,center=center,wrap=wrap,intensity=1,width=0.05*size)
        self.kernelD = FuncMapND(utils.gaussNd,"D_noiseK",size,dt=dt,center=center,wrap=wrap,intensity=1,width=0.1*size)
        
        irSensor = np.zeros((size))
        direction = np.zeros((size))
        
        self.getIRSensors = ConstantMap("IRSensors", size,value=irSensor)
        self.getDirection = ConstantMap("Direction",size, value=direction)
        
        self.navigationMap.addChildren(aff=self.navAffGain)
        self.navAff.addChildren(a=self.activationD, b=self.activationI)
        self.modelI.addChildren(source=self.getIRSensors, kernel=self.kernelI)
        self.modelD.addChildren(source=self.getDirection, kernel=self.kernelD)
        self.motorL.addChildren(activationI=self.navigationMap.getActivation(), activationD = self.activationD,simulator=self.simulator)
        self.motorR.addChildren(activationI=self.navigationMap.getActivation(), activationD = self.activationD,simulator=self.simulator)
        self.activationI.addChildren(dnfmapI=self.dnfmapI)
        self.activationD.addChildren(dnfmapD=self.dnfmapD)
        #self.getIRSensors.addChildren(simulator=self.simulator)
        #self.getDirection.addChildren(simulator=self.simulator)
        self.dnfmapI.addChildren(aff=self.modelI)
        self.dnfmapD.addChildren(aff=self.modelD)
        #return the roots
        roots =  [self.motorL, self.motorR]

        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.motorL, self.motorR, self.activationI, self.dnfmapI, self.modelI, self.activationD, self.dnfmapD,  self.modelD, self.kernelI,self.kernelD, self.navigationMap, self.navigationMap.getActivation(),self.navigationMap.kernel]

        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
        
    def _reset(self):
        super(ModelEPuckDNF,self)._reset(
        )
        #self.simulator.disconnection()
        #self.simulator.connection()
        
