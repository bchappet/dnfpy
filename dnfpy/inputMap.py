from map2D import Map2D
from funcMap2D import FuncMap2D
from funcWithoutKeywords import FuncWithoutKeywords
import numpy as np
import utils



def randomNormal(scale,size):
    """np.random.normal does not support scale = 0"""
    if scale == 0:
        return np.zeros(size,dtype=np.float32)
    else:
        return np.random.normal(scale=scale,size=size)



class InputMap(FuncWithoutKeywords):
    """The input are defined here"""
    def __init__(self,size,dt,globalRealParams):
        super(InputMap,self).__init__(size,dt,globalRealParams,utils.sumArrays)
        self.distrs = FuncWithoutKeywords(self.size,self.globalRealParams['distr_dt'],self.globalRealParams,utils.sumArrays)
        self.updateNbDistr(self.globalRealParams['nbDistr'])


        period = 36
        self.track1 = self.newTrack(0)
        self.track2 = self.newTrack(1)

        self.noise = FuncMap2D(self.size,self.globalRealParams['noise_dt'],self.globalRealParams,randomNormal,{'size':(self.size,self.size)})
        self.noise.registerOnGlobalParamsChange({'scale':'noiseI'})


        self.addChildren({'track1':self.track1,'track2':self.track2,'noise':self.noise,'distrs':self.distrs})

    def newTrack(self,index):
        dt = self.globalRealParams['tck_dt']
        period  = 36
        track = FuncMap2D(self.size,dt,self.globalRealParams,utils.gauss2d)
        track.registerOnGlobalParamsChange({'size':'size','wrap':'wrap','intensity':'iStim','width':'wStim'})

        center = (self.size-1)/2

        phase = index/2. + 0
        cX = FuncMap2D(1,dt,self.globalRealParams,utils.cosTraj,{'center':center,'period':period,'phase':phase})
        cX.registerOnGlobalParamsChange({'radius':'tck_radius'})
        cX.mapAttributesToFunc({'time':cX.getTime})

        phase = index/2. + 0.25
        cY = FuncMap2D(1,dt,self.globalRealParams,utils.cosTraj,{'center':center,'period':period,'phase':phase})
        cY.registerOnGlobalParamsChange({'radius':'tck_radius'})
        cY.mapAttributesToFunc({'time':cY.getTime})

        track.addChildren({'centerX':cX,'centerY':cY})
        return track

    def newDistr(self):
        dt = self.globalRealParams['distr_dt']
        distr = FuncMap2D(self.size,dt,self.globalRealParams,utils.gauss2d)
        distr.registerOnGlobalParamsChange({'size':'size','wrap':'wrap','intensity':'iDistr','width':'wDistr'})
        cX = FuncMap2D(1,dt,self.globalRealParams,np.random.uniform,{'high':self.size})
        cY = FuncMap2D(1,dt,self.globalRealParams,np.random.uniform,{'high':self.size})
        distr.addChildren({'centerX':cX,'centerY':cY})
        return distr

    def updateNbDistr(self,nb):
        while self.distrs.getChildrenCount() > nb:
            self.distrs.removeChild('distr'+str(self.distrs.getChildrenCount()-1))

        while self.distrs.getChildrenCount() < nb:
            distr = self.newDistr()
            self.distrs.addChildren({'distr'+str(self.distrs.getChildrenCount()):distr})


        




        
        


