from dnfpy.cellular.nSpikeMap import NSpikeMap
from dnfpy.cellular.rsdnfMap import RsdnfMap
import numpy as np
from dnfpy.core.map2D import Map2D


def normalizeProba(p,size):
    return p**(1./(size))

def normalizeIntensity(i,size,alpha,nspike):
    #print i,size,alpha,nspike
    res =  i/(size**2) * (40**2)/alpha * 1./nspike
    #print "res = ",res
    return res


class NSpikeConvolution(Map2D):
    """
    Children needed: "activation" with map of 0 and 1 of type np.intc
    """
    def __init__(self,name,size,dt=0.1,nspike=20,
                 iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.4,alpha=10,
                 iExc_=1.,iInh_=1.,pInh_=0.,pExc_=0.,
                 reproductible=True,cell='NSpike',clkRatio=50,#if cellular model, the cells will be computed 100 time betwenn each computation
                 routerType='prng',
                 **kwargs):
        super(NSpikeConvolution,self).__init__(name,size,dt=dt,nspike=nspike,
                iExc=iExc,iInh=iInh,pExc=pExc,pInh=pInh,alpha=alpha,
                 iExc_=iExc_,iInh_=iInh_,pInh_=pInh_,pExc_=pExc_,
                reproductible=reproductible,cell=cell,clkRatio=clkRatio,routerType=routerType,
                                               **kwargs)
        if cell is 'NSpike':
            self.inh = NSpikeMap(name+"_inh",size,dt=dt,nspike=nspike,
                                proba=pInh_,reproductible=reproductible)
            self.exc = NSpikeMap(name+"_exc",size,dt=dt,nspike=nspike,
                                proba=pExc_,reproductible=reproductible)
        elif cell is 'Rsdnf':
            dtCellular = dt / clkRatio
           

            self.inh = RsdnfMap(name+"_inh",size,dt=dtCellular,nspike=nspike,
                                proba=pInh_,reproductible=reproductible,clkRatio=clkRatio,routerType=routerType)
            self.exc = RsdnfMap(name+"_exc",size,dt=dtCellular,nspike=nspike,
                                proba=pExc_,reproductible=reproductible,clkRatio=clkRatio,routerType=routerType)
        else:
            raise NameError("the cell "+str(cell)+" does not exist. Try NSpike or Rsdnf." )

        self.addChildren(inhMap = self.inh,excMap = self.exc)



    def _compute(self,inhMap,excMap,iInh_,iExc_,activation):
        self._data = excMap *  iExc_ - inhMap * iInh_


    def resetLat(self):
        #we reset the data (NB_BIT_RECEIVED) of inh and exc when we integrate it
        #in the neural's potential
        self.inh.resetData()
        self.exc.resetData()


    def _onParamsUpdate(self,size,alpha,nspike,iExc,iInh,pExc,pInh):
        pExc_ = normalizeProba(pExc,size)
        pInh_ = normalizeProba(pInh,size)
        iExc_ = normalizeIntensity(iExc,size,alpha,nspike)
        iInh_ = normalizeIntensity(iInh,size,alpha,nspike)
        #print("pExc_ %s, pInh_ %s, iExc_ %s, iInh_ %s"%(pExc_,pInh_,iExc_,iInh_))

        return dict(pExc_=pExc_,pInh_=pInh_,iExc_=iExc_,iInh_=iInh_)

    def _childrenParamsUpdate(self,nspike,pInh_,pExc_):
        self.exc.setParams(nspike=nspike,proba=pExc_)
        self.inh.setParams(nspike=nspike,proba=pInh_)

    def _onAddChildren(self,**kwargs):
        if "activation" in kwargs.keys():
            actMap = kwargs.get("activation")
            self.exc.addChildren(activation=actMap)
            self.inh.addChildren(activation=actMap)
