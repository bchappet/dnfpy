import numpy as np
from dnfpy.model.straightTrack import StraightTrack
from dnfpy.model.noiseMapND import NoiseMap
from dnfpy.model.distrMapND import DistrMap
from dnfpy.core.funcWithoutKeywordsND import FuncWithoutKeywords
import dnfpy.core.utils as utils
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
                 tck_dt=0.1,iStims=[1.0,0.95],wStim=0.1,nbDistr=0,iDistr=0.99,tck_radius=0.3,
                 wDistr=0.1,wStim_=1.0,wDistr_=1.0,tck_radius_=1,periodStim=36,normalize=True,iStim=1.0,
                 straight=False,speed=0.04,nbTrack =2,position=None,
                 dvs=False,tauDVS=0.1,thDVS=0.7,blink=False,blinkPeriod=0.02,
                 **kwargs):
        super().__init__(utils.sumArrays,name,size,dim=dim,dt=dt,
                wrap=wrap,distr_dt=distr_dt,noise_dt=noise_dt,noiseI=noiseI,
                tck_dt = tck_dt,  wStim = wStim ,wDistr=wDistr,
                nbDistr = nbDistr ,iDistr=iDistr,tck_radius = tck_radius,nbTrack=nbTrack,
                wStim_=wStim_,wDist_=wDistr_,tck_radius_=tck_radius_,periodStim=periodStim,
                straight=straight,speed=speed,
                normalize=normalize,dvs=dvs,tauDVS=tauDVS,thDVS=thDVS,position=position,
                blink=blink,blinkPeriod=blinkPeriod,
                **kwargs)



        self.distrs = DistrMap("Distracters",size,dim=dim,dt=distr_dt,wrap=wrap,
                        intensity=iDistr,width=wDistr_,number=nbDistr)
        self.noise = NoiseMap("noise",size,dim=dim,dt=noise_dt,intensity=noiseI)


        #self.traj = []
        self.tracks = []

        if straight:
            direction = np.float32([1]*dim)
            if position == None:
                dPos = 1/nbTrack
                position = [np.array((0.2+i*dPos,)*dim) for i in range(nbTrack)]
            for i in range(nbTrack):
                self.tracks.append(StraightTrack(self.getName()+"_track"+str(i),size=size,dim=dim,dt=tck_dt,wrap=wrap,intensity=iStims[i],width=wStim,direction=direction,start=position[i],speed=speed,blink=blink,blinkPeriod=blinkPeriod))
        else:
            for i in range(nbTrack):
                self.tracks.append(self.newTrack(i,size,dim,tck_dt,wrap,iStims[i],wStim,tck_radius,periodStim,blink,blinkPeriod))


        self.addChildren(self.noise,self.distrs,*self.tracks)


    def _compute(self,args,params):
        super()._compute(args,params)
        if self.getArg('normalize'):
            self._data = np.clip(self._data,-1,1)
        if self.getArg('dvs'):
            dt,tauDVS,thDVS = self.getArgs('dt','tauDVS','thDVS')
            self.dvsPotential += dt/tauDVS*(self._data - self.dvsPotential)
            self._data = np.where(self.dvsPotential >= thDVS,1.0,0.0)
            self.dvsPotential[self._data == 1.0] = 0.0; #reset

    def reset(self):
        super().reset()
        if self.getArg('dvs'):
            size,dim = self.getArgs('size','dim')
            self.dvsPotential = np.zeros((size,)*dim)


        #debug:
    def get_nbDistr(self):
        return self.distrs.getArg('number')

    def getTracks(self):
        return self.tracks

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
                              wStim_,tck_radius_,noise_dt,noiseI,periodStim):


        self.noise.setParams(dt=noise_dt,scale=noiseI)
        self.distrs.setParams(dt=distr_dt,wrap=wrap,intensity=iDistr,width=wDistr_,
                        number=nbDistr)
        for track in self.tracks:
            track.setParams(dt=tck_dt)
            #TODO do something to avoid this (we got to change dt recursevly in some case)
            for child in track.getChildren().values():
                    child.setParams(dt=tck_dt)



    def newTrack(self,index,size,dim,tck_dt,wrap,iStim,wStim,tck_radius,periodStim,blink,blinkPeriod):
        name = self.getName() +  "_track"+str(index)
        phase = index/2.
        period  = periodStim
        track = CircularTrack(name,size,dim=dim,dt=tck_dt,wrap=wrap,intensity=iStim,
                    width=wStim,radius=tck_radius,period=period,phase=phase,blink=blink,blinkPeriod=blinkPeriod)

        return track
