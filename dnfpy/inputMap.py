from map2D import Map2D
from funcMap2D import FuncMap2D
from funcWithoutKeywords import FuncWithoutKeywords
import random
import numpy as np
import utils



def randomNormal(scale,size_):
    """np.random.normal does not support scale = 0"""
    if scale == 0:
        return np.zeros(size_,dtype=np.float32)
    else:
        return np.random.normal(scale=scale,size=size_)

class InputMap(FuncWithoutKeywords):
    """The input are defined here"""
    def __init__(self,size,**kwargs):
        super(InputMap,self).__init__(utils.sumArrays,size,**kwargs)
        self.distrs = FuncWithoutKeywords(utils.sumArrays,self._getArg('size'))
        self.distrs.registerOnGlobalParamsChange_ignoreCompute(dt='distr_dt')

        self.track1 = self.newTrack(0)
        self.track2 = self.newTrack(1)

        self.noise = FuncMap2D(randomNormal,self._getArg('size'),size_=(size,size))
        self.noise.registerOnGlobalParamsChange(dt='noise_dt',scale='noiseI')

        self.addChildren(track1=self.track1,track2=self.track2,noise=self.noise,distrs=self.distrs)

    def _onParamUpdate(self):
        self.updateNbDistr(self._getArg('nb_distr'))


    def newTrack(self,index):
        period  = 36
        track = FuncMap2D(utils.gauss2d,self._getArg('size'))
        track.registerOnGlobalParamsChange(dt='tck_dt',wrap='wrap',intensity='iStim',width='wStim')

        center = (self._getArg('size')-1)/2

        phase = index/2. + 0
        cX = FuncMap2D(utils.cosTraj,1,center=center,period=period,phase=phase)
        cX.registerOnGlobalParamsChange(dt='tck_dt',radius='tck_radius')

        phase = index/2. + 0.25
        cY = FuncMap2D(utils.cosTraj,1,center=center,period=period,phase=phase)
        cY.registerOnGlobalParamsChange(dt='tck_dt',radius='tck_radius')

        track.addChildren(centerX=cX,centerY=cY)
        return track

    def newDistr(self):
        distr = FuncMap2D(utils.gauss2d,self._getArg('size'))
        distr.registerOnGlobalParamsChange(dt='distr_dt',wrap='wrap',intensity='iDistr',width='wDistr')
        cX = FuncMap2D(random.uniform,1,a=0,b=self._getArg('size'))
        cX.registerOnGlobalParamsChange(dt='distr_dt')
        cY = FuncMap2D(random.uniform,1,a=0,b=self._getArg('size'))
        cY.registerOnGlobalParamsChange(dt='distr_dt')
        distr.addChildren(centerX=cX,centerY=cY)
        return distr

    def updateNbDistr(self,nb):
        while self.distrs.getChildrenCount() > nb:
            self.distrs.removeChild('distr'+str(self.distrs.getChildrenCount()-1))

        while self.distrs.getChildrenCount() < nb:
            distr = self.newDistr()
            self.distrs.addChildren(**{'distr'+str(self.distrs.getChildrenCount()):distr})

