import numpy as np
from dnfpy.core.map2D import Map2D
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.activationMap import ActivationMap
from dnfpy.model.fieldMap import FieldMap
from dnfpy.model.mapSFA import MapSFA
from dnfpy.model.lateralWeightsMap import LateralWeightsMap
from dnfpy.model.convolution import Convolution
from dnfpy.core.funcWithoutKeywords import FuncWithoutKeywords
import dnfpy.core.utils as utils


class  AffSFA(Map2D):
    def __init__(self,name,size,dt,beta):
        super(AffSFA,self).__init__(name,size,dt=dt,beta=beta)

    def _compute(self,beta,input,sfa):
        self._data = ((1-beta))*2*input - (beta)*2*sfa

class SFAMap(Map2D):
    def __init__(self,name,size,dt,tau=1.,m=6.4):
        super(SFAMap,self).__init__(name=name,size=size,dt=dt,tau=tau,m=m)

    def _compute(self,pot,tau,dt,m):
        self._data = self._data + dt/tau*(-self._data + m*pot)


class ModelSFA(Model,Renderable):
    """
    This model is using Spike Frequency adaptation to improve the tracking.
    It is very efficient

    """
    def initMaps(self,size=49,model="spike",nbStep=0,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10.,alpha=10.,
                 obsSize=0.50,nbDistr=0,m=1.1,tauSFA=2.8,
                 ):
        """We initiate the map and link them"""
       # print("iExc : %s, iInh: %s, wExc %s, wInh %s"%(iExc,iInh,wExc,wInh))
        #Create maps
        dt = 0.1
        wrap=True
        th = 0.75


        #self.aff = AffSFA("AffSFA",size,dt=dt,beta=0.20)
        #self.aff.addChildren(input=self.input)

        #self.sfa = SFAMap("SFAMap",size,dt=dt,tau=2.8,m=1.1)
        #self.aff.addChildren(sfa=self.sfa)



        #self.act = ActivationMap("DNF_activation",size,dt=dt,model=model,th=th)
        #self.lat = Convolution("DNF_lateral",size,dt=dt,wrap=wrap)
        #self.kernel = LateralWeightsMap("DNF_kernel",mapSize=1.,
        #                                globalSize=size,wrap=wrap,
        #                                iExc=iExc,iInh=iInh,wExc=wExc,
        #                                wInh=wInh,alpha=alpha,nbStep=nbStep)
        #self.lat.addChildren(source=self.act,kernel=self.kernel)

        #self.field = FieldMap("DNF",size,model=model,nbStep=nbStep, \
        #                iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh,th=th)
        #self.field.addChildren(aff=self.aff)
        #self.field.addChildren(lat=self.lat)


        #self.act.addChildren(field=self.field)

        #self.sfa.addChildren(pot=self.field)
        self.field =  MapSFA("dnfSFA",size,dt=dt,wrap=wrap,model=model,th=th,iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh,m=m,tauSFA=tauSFA)
        self.field.addChildren(aff=self.input)
        #stats
        self.stats = StatsList(size,self.input,self.field.getActivation(),
                               self.field,shapeType='gauss')
        #return the roots
        roots =  [self.field]
        roots.extend(self.stats.getRoots())
        return roots

    #override Renderable
    def getArrays(self):
        #ret =  [self.input,self.sfa,self.aff,self.field,self.act,self.lat]
        ret = [self.input,self.field]
        ret.extend(self.field.getArrays())
        ret.extend(self.stats.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
