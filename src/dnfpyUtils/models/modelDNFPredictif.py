from dnfpy.model.inputMap import InputMap
from dnfpy.model.straightTrack import StraightTrack
import numpy as np
from dnfpy.core.map2D import Map2D
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.stats.statsList import StatsList
from dnfpy.model.activationMap import ActivationMap
from dnfpy.model.fieldMap import FieldMap
from dnfpy.model.lateralWeightsMap import LateralWeightsMap
from dnfpy.model.convolution import Convolution
from dnfpy.core.funcWithoutKeywords import FuncWithoutKeywords
import dnfpy.core.utils as utils


class  AffPred(Map2D):
    def __init__(self,name,size,dt,beta):
        super(AffPred,self).__init__(name,size,dt=dt,beta=beta)

    def _compute(self,beta,input,prediction):
        self._data = beta*prediction + (1-beta)*input

class PredMap(Map2D):
    def __init__(self,name,size,dt,speed=0.01,direction=np.float32([1.,1.])):
        super(PredMap,self).__init__(name=name,size=size,dt=dt,speed=speed,
                                     direction=direction)

    def _compute(self,size,ref,speed,direction):
        #transform speed vec in pixel per second
        #print("speed : %s, size: %s, direction: %s"%(speed,size,direction))
        speedVec = speed * size * direction
        self._data = utils.matrixTranslation(ref,speedVec[1],speedVec[0])



class ModelDNFPredictif(Model,Renderable):
    def initMaps(self,size=49,model="cnft",nbStep=0,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10.,alpha=10.,
                 ):
        """We initiate the map and link them"""
       # print("iExc : %s, iInh: %s, wExc %s, wInh %s"%(iExc,iInh,wExc,wInh))
        #Create maps
        dt = 0.1
        wrap=True
        th = 0.75
        #self.input = InputMap("Inputs",size)
        self.input = StraightTrack("input",size,dt,wrap,1.,width=0.1,
                                    direction=np.float32([1,1]),speed=0.04)


        self.aff = AffPred("AffPred",size,dt=dt,beta=0.5)
        self.aff.addChildren(input=self.input)

        self.pred = PredMap("PredMap",size,dt=dt,speed=0.06)
        self.aff.addChildren(prediction=self.pred)



        self.act = ActivationMap("DNF_activation",size,dt=dt,model=model,th=th)
        self.lat = Convolution("DNF_lateral",size,dt=dt,wrap=wrap)
        self.kernel = LateralWeightsMap("DNF_kernel",mapSize=1.,
                                        globalSize=size,wrap=wrap,
                                        iExc=iExc,iInh=iInh,wExc=wExc,
                                        wInh=wInh,alpha=alpha,nbStep=nbStep)
        self.lat.addChildren(source=self.act,kernel=self.kernel)

        self.field = FieldMap("DNF",size,model=model,nbStep=nbStep, \
                        iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh)
        self.field.addChildren(aff=self.aff)
        self.field.addChildren(lat=self.lat)


        self.act.addChildren(field=self.field)

        self.pred.addChildren(ref=self.act)
        #stats
        self.stats = StatsList(size,self.input,self.act,
                               self.kernel,self.field,shapeType='gauss')
        #return the roots
        roots =  [self.field]
        roots.extend(self.stats.getRoots())
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.input,self.pred,self.aff,self.field,self.act,self.lat]
        ret.extend(self.stats.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
