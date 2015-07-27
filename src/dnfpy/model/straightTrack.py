import numpy as np
from dnfpy.core.funcMap2D import FuncMap2D
import dnfpy.core.utils as utils
from dnfpy.core.map2D import Map2D




class StraightTrack(Map2D):
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
    def __init__(self,name,size,dt=0.1,wrap=True,intensity=1.,width=0.1,
                 direction=np.float32([1,1]),start = np.float32([0,0]),
                 speed=0.01,speedX_=1.,speedY_=1.):
        super(StraightTrack,self).__init__(name=name,size=size,
                                           dt=dt,wrap=wrap,intensity=intensity,
                                           width=width,direction=direction,
                                           start=start,
                                           speed=speed,speedX_=speedX_,
                                           speedY_=speedY_)


        self.cX = FuncMap2D(utils.affTraj,name+"_cX",1,dt=dt,speed=speedX_,origin=start[1]*size,
                        wrap=wrap,wrapSize=size)
        self.cY = FuncMap2D(utils.affTraj,name+"_cY",1,dt=dt,speed=speedY_,origin=start[0]*size,
                        wrap=wrap,wrapSize=size)

        self.addChildren(centerX=self.cX,centerY=self.cY)

    def _onParamsUpdate(self,size,width,speed,direction):
        width_ = width * size
        speedY_ = speed * size*direction[0] #pixel per sec
        speedX_ = speed * size*direction[1] #pixel per sec
        return dict(width_=width_,speedX_=speedX_,speedY_=speedY_)

    def _childrenParamsUpdate(self,speedX_,speedY_):
        self.cX.setParams(speed=speedX_)
        self.cY.setParams(speed=speedY_)

    def _compute(self,size,wrap,width_,intensity,centerX,centerY):
        self._data = utils.gauss2d(size,wrap,intensity,width_,centerX,centerY)

    def getTracks(self):
        return [self,]

    def getWidth(self):
        return self.getArg('width_')

    def getIntensity(self):
        return self.getArg('intensity')


