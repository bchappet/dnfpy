from dnfpy.core.funcMap2D import FuncMap2D
from noiseMap import NoiseMap
from distrMap import DistrMap
from dnfpy.core.funcWithoutKeywords import FuncWithoutKeywords
import dnfpy.core.utils as utils
import random
import numpy as np
import copy

class PlayCamMap(FuncWithoutKeywords):
    """The input are defined here"""
    def __init__(self,name,size,dt=0.1,wrap=True,distr_dt=1.0,noise_dt=0.2,noiseI=0.01,
                 tck_dt=0.1,iStim=1.0,wStim=0.1,nbDistr=0,iDistr=1.0,tck_radius=0.3,
                 wDistr=0.1,wStim_=1,wDistr_=1,tck_radius_=1,**kwargs):
        super(PlayCamMap,self).__init__(utils.sumImageArrays,name,size,dt=dt,
                wrap=wrap,distr_dt=distr_dt,noise_dt=noise_dt,noiseI=noiseI,
                tck_dt = tck_dt,iStim = iStim ,wStim = wStim ,wDistr=wDistr,
                nbDistr = nbDistr ,iDistr=iDistr,tck_radius = tck_radius,
                wStim_=wStim_,wDist_=wDistr_,tck_radius_=tck_radius_,
                **kwargs)
        self.distrs = DistrMap("Distracters",size,dt=distr_dt,wrap=wrap,
                        intensity=iDistr,width=wDistr_,number=nbDistr)

        self.noise = NoiseMap("noise",size,dt=noise_dt,intensity=noiseI)

        self.addChildren(self.noise,self.distrs)

        #debug:
    def get_nbDistr(self):
        return self.distrs.getChildrenCount()

    def _onParamsUpdate(self,size,nbDistr,wStim,wDistr,tck_radius):
        wStim_ = wStim * size
        wDistr_ = wDistr *size
        tck_radius_ = tck_radius * size
        return dict(wStim_=wStim_,wDistr_=wDistr_,tck_radius_=tck_radius_)

    def _childrenParamsUpdate(self,size,distr_dt,tck_dt,wrap,iDistr,wDistr_,nbDistr,
                              wStim_,tck_radius_,iStim,noise_dt,noiseI):

        self.noise.setParams(dt=noise_dt,scale=noiseI)
        self.distrs.setParams(dt=distr_dt,wrap=wrap,intensity=iDistr,width=wDistr_,
                        number=nbDistr)

