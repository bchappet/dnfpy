
from dnfpy.core.funcMap2D import FuncMap2D
import dnfpy.core.utils as utils
from dnfpy.core.mapND import MapND
import numpy as np




class CircularTrack(MapND):
    """
    Circular gaussian shaped trajectory
    ====================================
    Params:

    intensity : of the gaussian
    width : of the gaussian
    radius : of the circle in [0,1]
    center : of the circle in [-1,1]
    period : of the circle
    phase : of the circle
    ====================================
    Computed params:

    width_
    radius_
    center_
    ====================================
    Children:

    default:
    centerX : cos traj
    centerY : cos traj
    """
    def __init__(self,name,size,dim=2,dt=0.1,wrap=True,intensity=1.,width=0.1,
                 radius=0.3,period=36,phase=0.,center=0.,
                 center_=10,radius_=10):
        super().__init__(name=name,size=size,dim=dim,
                                           dt=dt,wrap=wrap,intensity=intensity,
                                           width=width,radius=radius,center=center,
                                           period=period,phase=phase,
                                           center_=center_,radius_=radius_)

        self.cX = FuncMap2D(utils.cosTraj,name+"_cX",1
                       ,center=center_,period=period,phase=phase,
            dt=dt,radius=radius_)
        self.cY = FuncMap2D(utils.cosTraj,name+"_cY",1,
                       center=center_,period=period,phase=phase+0.25,
            dt=dt,radius=radius_)

        self.addChildren(centerX=self.cX,centerY=self.cY)

    def _onParamsUpdate(self,size,width,radius,center):
        width_ = width * size
        radius_ = radius * size
        center_ = center * size + (size-1)/2
        return dict(width_=width_,radius_=radius_,center_=center_)

    def _childrenParamsUpdate(self,radius_,center_):
        self.cX.setParams(radius=radius_,center=center_)
        self.cY.setParams(radius=radius_,center=center_)

    def _compute(self,size,wrap,width_,intensity,centerX,centerY):
        self._data = utils.gauss2d(size,wrap,intensity,width_,centerX,centerY)

    def getCenter(self):
            return np.array([self.cX.getData(),self.cY.getData()])

    def getShape(self):
            return self.getArg('intensity'),self.getArg('width_')
