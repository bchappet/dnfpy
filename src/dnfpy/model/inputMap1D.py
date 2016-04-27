import numpy as np
from dnfpy.model.straightTrack import StraightTrack
from dnfpy.core.funcMapND import FuncMapND
from dnfpy.model.noiseMapND import NoiseMap
from dnfpy.model.distrMapND import DistrMap
from dnfpy.core.funcWithoutKeywordsND import FuncWithoutKeywords
import dnfpy.core.utilsND as utils
from dnfpy.model.circularTrack1D import CircularTrack
from dnfpy.core.mapND import MapND

class ObstacleMap(MapND):
    """
    Put data to zero somewhere
    """
    def __init__(self,name,size,dt=0.1,obsSize=0.2,**kwargs):
        super(ObstacleMap,self).__init__(name,size,dt=dt,obsSize=obsSize,dtype=np.bool,**kwargs)

    def _compute(self,size,input2,obsSize):
        size2 = (size-1)/2
        obsize2 = int((size*obsSize - 1) /2)
        self._data = input2
        self._data[size2-obsize2:size2+obsize2,:] = 0


    def getTracks(self):
        return self.getChild('input2').getTracks()

    def getWidth(self):
        return self.getChild('input2').getWidth()

    def getIntensity(self):
        return self.getChild('input2').getIntensity()


class InputMap(FuncWithoutKeywords):
    """The input are defined here"""
    def __init__(self,name,size,dim=1,dt=0.1,wrap=True,distr_dt=1.,noise_dt=0.1,noiseI=0.01,
                 tck_dt=0.1,iStim1=0.99,iStim2=0.99,wStim=0.1,nbDistr=0,iDistr=0.99,tck_radius=0.3,
                 wDistr=0.1,wStim_=1.0,wDistr_=1.0,tck_radius_=1,periodStim=36,normalize=True,iStim=1.0,
                 straight=False,speed=0.04,
                 **kwargs):
        super(InputMap,self).__init__(utils.sumArrays,name,size,dim=dim,dt=dt,
                wrap=wrap,distr_dt=distr_dt,noise_dt=noise_dt,noiseI=noiseI,
                tck_dt = tck_dt,iStim1 = iStim1, iStim2 = iStim2, wStim = wStim ,wDistr=wDistr,
                nbDistr = nbDistr ,iDistr=iDistr,tck_radius = tck_radius,
                wStim_=wStim_,wDist_=wDistr_,tck_radius_=tck_radius_,periodStim=periodStim,
                                      iStim=iStim,straight=straight,speed=speed,
                normalize=normalize,
                **kwargs)


        self.distrs = DistrMap("Distracters",size,dim=dim,dt=distr_dt,wrap=wrap,
                        intensity=iDistr,width=wDistr_,number=nbDistr)
        self.noise = NoiseMap("noise",size,dim=dim,dt=noise_dt,intensity=noiseI)


        #self.traj = []

        if straight:
            direction = np.float32([1]*dim)
            self.track1 = StraightTrack(self.getName()+"_track0",size=size,dim=dim,dt=tck_dt,wrap=wrap,intensity=iStim1,width=wStim,
                                    direction=direction,start=np.array([0.2,0.2]),speed=speed)
            self.track2 = StraightTrack(self.getName()+"_track1",size=size,dim=dim,dt=tck_dt,wrap=wrap,intensity=iStim2,width=wStim,
                                    direction=direction,start=np.array([0.5,0.5]),speed=speed)
        else:
            self.track1 = self.newTrack(0,size,dim,tck_dt,wrap,iStim1,wStim,tck_radius,periodStim)
            self.track2 = self.newTrack(1,size,dim,tck_dt,wrap,iStim2,wStim,tck_radius,periodStim)






        self.addChildren(self.track1,self.track2,self.noise,self.distrs)


    def _compute(self,args):
        super(InputMap,self)._compute(args)
        if self.getArg('normalize'):
            self._data = np.clip(self._data,-1,1)



        #debug:
    def get_nbDistr(self):
        return self.distrs.getArg('number')

    def getTracks(self):
        tracks = []
        if self.track1:
            tracks.append(self.track1)
        if self.track2:
            tracks.append(self.track2)
        return tracks

    def getWidth(self):
        return self.getArg('wStim_')

    def getIntensity(self):
        return self.getArg('iStim')

    def _onParamsUpdate(self,size,wStim,wDistr,tck_radius):
        wStim_ = wStim * size
        wDistr_ = wDistr *size
        tck_radius_ = tck_radius * size
        return dict(wStim_=wStim_,wDistr_=wDistr_,tck_radius_=tck_radius_)

    def _childrenParamsUpdate(self,size,distr_dt,tck_dt,wrap,iDistr,wDistr_,nbDistr,
                              wStim_,tck_radius_,iStim1,iStim2,noise_dt,noiseI,periodStim):

        #self.track1.setParams(wrap=wrap,dt=tck_dt,intensity=iStim1,
        #                   width=wStim_,periodStim=periodStim)
        #self.track2.setParams(wrap=wrap,dt=tck_dt,intensity=iStim2,
        #                   width=wStim_,periodStim=periodStim)
        #for t in self.traj:
        #    t.setParams(radius=tck_radius_)

        self.noise.setParams(dt=noise_dt,scale=noiseI)
        self.distrs.setParams(dt=distr_dt,wrap=wrap,intensity=iDistr,width=wDistr_,
                        number=nbDistr)
        if self.track1:
            self.track1.setParams(dt=tck_dt)
            #TODO do something to avoid this (we got to change dt recursevly in some case)
            for child in self.track1.getChildren().values():
                    child.setParams(dt=tck_dt)

        if self.track2:
            self.track2.setParams(dt=tck_dt)
            for child in self.track2.getChildren().values():
                    child.setParams(dt=tck_dt)
            



    def newTrack(self,index,size,dim,tck_dt,wrap,iStim,wStim,tck_radius,periodStim):
        name = self.getName() +  "_track"+str(index)
        phase = index/2.
        period  = periodStim
        track = CircularTrack(name,size,dim=dim,dt=tck_dt,wrap=wrap,intensity=iStim,
                    width=wStim,radius=tck_radius,period=period,phase=phase)

        return track
