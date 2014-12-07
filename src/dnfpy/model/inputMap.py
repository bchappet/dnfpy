from dnfpy.core.funcMap2D import FuncMap2D
from noiseMap import NoiseMap
from distrMap import DistrMap
from dnfpy.core.funcWithoutKeywords import FuncWithoutKeywords
import dnfpy.core.utils as utils
import random
import numpy as np
import copy




class InputMap(FuncWithoutKeywords):
    """The input are defined here"""
    def __init__(self,name,size,dt=0.1,wrap=True,distr_dt=0.1,noise_dt=0.1,noiseI=0.01,
                 tck_dt=0.1,iStim=1,wStim=0.1,nbDistr=0,iDistr=1,tck_radius=0.3,
                 wDistr=0.1,wStim_=1,wDistr_=1,tck_radius_=1,**kwargs):
        super(InputMap,self).__init__(utils.sumArrays,name,size,dt=dt,
                wrap=wrap,distr_dt=distr_dt,noise_dt=noise_dt,noiseI=noiseI,
                tck_dt = tck_dt,iStim = iStim ,wStim = wStim ,wDistr=wDistr,
                nbDistr = nbDistr ,iDistr=iDistr,tck_radius = tck_radius,
                wStim_=wStim_,wDist_=wDistr_,tck_radius_=tck_radius_,
                **kwargs)
        self.distrs = DistrMap("Distracters",size,dt=distr_dt,wrap=wrap,
                        intensity=iDistr,width=wDistr_,number=nbDistr)


        self.traj = []
        self.track1 = self.newTrack(0,size,tck_dt,wrap,iStim,wStim_,tck_radius_)
        self.track2 = self.newTrack(1,size,tck_dt,wrap,iStim,wStim_,tck_radius_)

        self.noise = NoiseMap("noise",size,dt=noise_dt,intensity=noiseI)

        self.addChildren(track1=self.track1,track2=self.track2,
                         noise=self.noise,distrs=self.distrs)

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

        self.track1.setParams(wrap=wrap,dt=tck_dt,intensity=iStim,
                           width=wStim_)
        self.track2.setParams(wrap=wrap,dt=tck_dt,intensity=iStim,
                           width=wStim_)
        for t in self.traj:
            t.setParams(radius=tck_radius_)
        self.noise.setParams(dt=noise_dt,scale=noiseI)
        self.distrs.setParams(dt=distr_dt,wrap=wrap,intensity=iDistr,width=wDistr_,
                        number=nbDistr)



    def newTrack(self,index,size,tck_dt,wrap,iStim,wStim_,tck_radius_):
        name = self.getName() +  "_track"+str(index)
        period  = 36
        track = FuncMap2D(utils.gauss2d,name,
                          size,dt=tck_dt,wrap=wrap,
                          intensity=iStim,width=wStim_)

        center = (size-1)/2

        phase = index/2. + 0
        cX = FuncMap2D(utils.cosTraj,name+"_cX",1
                       ,center=center,period=period,phase=phase,
            dt=tck_dt,radius=tck_radius_)

        phase = index/2. + 0.25
        cY = FuncMap2D(utils.cosTraj,name+"_cY",1,center=center,period=period,phase=phase,
            dt=tck_dt,radius=tck_radius_)


        self.traj.append(cX)#TODO make it better
        self.traj.append(cY)
        track.addChildren(centerX=cX,centerY=cY)
        return track
