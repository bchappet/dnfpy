import numpy as np
from dnfpy.core.funcMapND import FuncMapND
import dnfpy.core.utilsND as utils
from dnfpy.core.mapND import MapND


class StraightTraj(MapND):
    def _compute(self,speed,dt,wrap,wrapSize):
        self._data = (self._data + dt*speed)
        if wrap:
            self._data = self._data % wrapSize


#TODO super class for track
class StraightTrack(MapND):
    """
    Straight gaussian shaped trajectory
    ====================================
    Params:

    intensity : of the gaussian
    width : of the gaussian
    direction : vector
    speed in map size per second
    ====================================
    Computed params:

    width_
    speed_
    """
    def __init__(self,name,size,dim=1,dt=0.1,wrap=True,intensity=1.,width=0.1,
                 direction=np.float32((1,)*10),start = np.float32((0,)*10),
                 speed=0.01,speed_=(1,)*10):
        super().__init__(name=name,size=size,dim=dim,
                                           dt=dt,wrap=wrap,intensity=intensity,
                                           width=width,direction=direction,
                                           start=start,
                                           speed=speed,
                                           speed_=speed_)


        
        self.centerTraj = []
        for d in range(dim):
            origin = start[d]*size
            self.centerTraj.append(StraightTraj(name+"_c"+str(d),size=0,dim=0,dt=dt,speed=speed_[d],
                        wrap=wrap,wrapSize=size,init=origin))

        for trajI,i in zip(self.centerTraj,range(len(self.centerTraj))):
                self.addChildren(**{'center'+str(i):trajI})

    def _onParamsUpdate(self,size,width,speed,direction):
        width_ = width * size
        speed_ = []
        for i in range(len(direction)):
            speed_.append(speed * size*direction[i]) #pixel per sec
        return dict(width_=width_,speed_=speed_)

    def _childrenParamsUpdate(self,speed_):
        for trajI,i in zip(self.centerTraj,range(len(speed_))):
            trajI.setParams(speed=speed_[i])

    def _compute(self,size,wrap,width_,intensity):
        center = self.getCenter()
        self._data = utils.gaussNd(size,wrap,intensity,width_,center)

    def getTracks(self):
        return [self,]

    def getShape(self):
            return self.getArg('intensity'),self.getArg('width_')

    def getCenter(self):
        return np.array([traj.getData() for traj in self.centerTraj])

   

