from dnfpy.core.funcMap2D import FuncMap2D
from dnfpy.core.funcWithoutKeywords import FuncWithoutKeywords
import dnfpy.core.utils as utils
import random
import numpy as np



def randomNormal(scale,size_):
    """because np.random.normal does not support scale = 0"""
    if scale == 0:
        return np.zeros(size_,dtype=np.float32)
    else:
        return np.random.normal(scale=scale,size=size_)

class InputMap(FuncWithoutKeywords):
    """The input are defined here"""
    def __init__(self,size,dt=0.1,wrap=True,distr_dt=0.1,noise_dt=0.1,noiseI=0.01,
                 tck_dt=0.1,iStim=1,wStim=0.1,nbDistr=0,iDistr=1,tck_radius=0.3,
                 wDistr=0.1,**kwargs):
        super(InputMap,self).__init__(utils.sumArrays,size,dt=dt,
                wrap=wrap,distr_dt=distr_dt,noise_dt=noise_dt,noiseI=noiseI,
                tck_dt = tck_dt,iStim = iStim ,wStim = wStim ,wDistr=wDistr,
                nbDistr = nbDistr ,iDistr=iDistr,tck_radius = tck_radius,**kwargs)
        self.distrs = FuncWithoutKeywords(utils.sumArrays,size,dt=distr_dt)

        self.traj = []
        self.track1 = self.newTrack(0,size,tck_dt,wrap,iStim,wStim,tck_radius)
        self.track2 = self.newTrack(1,size,tck_dt,wrap,iStim,wStim,tck_radius)

        self.noise = FuncMap2D(randomNormal,size,
                         dt=noise_dt,scale=noiseI,size_=(size,size))

        self.addChildren(track1=self.track1,track2=self.track2,
                         noise=self.noise,distrs=self.distrs)

        #debug:
    def get_nbDistr(self):
        return self.distrs.getChildrenCount()

    def _onParamsUpdate(self,size,nbDistr,wStim,wDistr,tck_radius):
        wStim *= size
        wDistr *= size
        tck_radius *= size
        return dict(wStim=wStim,wDistr=wDistr,tck_radius=tck_radius)

    def _childrenParamsUpdate(self,size,distr_dt,tck_dt,wrap,iDistr,wDistr,nbDistr,
                              wStim,tck_radius,iStim):
        distrChildren = self.distrs.getChildren()
        for distr in distrChildren:
            distrChildren[distr].setArg(dt=distr_dt,wrap=wrap,iDistr=iDistr,wDistr=wDistr)
        self.track1.setArg(wrap=wrap,dt=tck_dt,intensity=iStim,
                           width=wStim)
        self.track2.setArg(wrap=wrap,dt=tck_dt,intensity=iStim,
                           width=wStim)
        for t in self.traj:
            t.setArg(radius=tck_radius)

        self.updateNbDistr(nbDistr,size,distr_dt,wrap,iDistr,wDistr)


    def newTrack(self,index,size,tck_dt,wrap,iStim,wStim,tck_radius):
        period  = 36
        track = FuncMap2D(utils.gauss2d,size,dt=tck_dt,wrap=wrap,
                          intensity=iStim,width=wStim)

        center = (size-1)/2

        phase = index/2. + 0
        cX = FuncMap2D(utils.cosTraj,1,center=center,period=period,phase=phase,
            dt=tck_dt,radius=tck_radius)

        phase = index/2. + 0.25
        cY = FuncMap2D(utils.cosTraj,1,center=center,period=period,phase=phase,
            dt=tck_dt,radius=tck_radius)


        self.traj.append(cX)#TODO make it better
        self.traj.append(cY)
        track.addChildren(centerX=cX,centerY=cY)
        return track

    def newDistr(self,size,distr_dt,wrap,iDistr,wDistr):
        distr = FuncMap2D(utils.gauss2d,size,dt=distr_dt,
                          wrap=wrap,intensity=iDistr,width=wDistr)
        cX = FuncMap2D(random.uniform,1,dt=distr_dt,a=0,b=size)
        cY = FuncMap2D(random.uniform,1,dt=distr_dt,a=0,b=size)
        distr.addChildren(centerX=cX,centerY=cY)
        return distr

    def updateNbDistr(self,nb,size,distr_dt,wrap,iDistr,wDistr):
        while self.distrs.getChildrenCount() > nb:
            self.distrs.removeChild('distr'+str(self.distrs.getChildrenCount()-1))

        while self.distrs.getChildrenCount() < nb:
            distr = self.newDistr(size,distr_dt,wrap,iDistr,wDistr)
            self.distrs.addChildren(**{'distr'+str(self.distrs.getChildrenCount()):distr})
