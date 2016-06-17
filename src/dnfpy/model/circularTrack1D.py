
import numpy as np
from dnfpy.core.funcMapND import FuncMap
import dnfpy.core.utils as utils
from dnfpy.core.mapND import MapND




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
    def __init__(self,name,size,dim=1,dt=0.1,wrap=True,intensity=1.,width=0.1,
                 radius=0.3,period=36,phase=0.,center=0.,blink=False,blinkPeriod=0.2,
                 center_=10,radius_=10,oscil=False):
        super(CircularTrack,self).__init__(name=name,size=size,dim=dim,
                                           dt=dt,wrap=wrap,intensity=intensity,
                                           width=width,radius=radius,center=center,
                                           period=period,phase=phase,
                                           blink=blink,
                                           blinkPeriod = blinkPeriod,oscil=oscil,
                                           center_=center_,radius_=radius_)

        self.centerTraj = []
        self._blinkCounter = 0;#TODO reset
        self._hidden = False #true when hidden pahse of blinking

        if oscil :
            self.iTraj = FuncMap(utils.cosTraj,name+"_i",1,dim=0,center=0.7,period=20,
                phase = 0,dt=dt,radius=0.3)
            self.addChildren(intensity=self.iTraj)
        
        for d in range(dim):
            self.centerTraj.append(FuncMap(utils.cosTraj,name+"_c"+str(d),1,dim=0,
                        center=center_,period=period,phase=phase+d*0.25,
                        dt=dt,radius=radius_))

        for trajI,i in zip(self.centerTraj,range(len(self.centerTraj))):
                self.addChildren(**{'center'+str(i):trajI})

    def _onParamsUpdate(self,size,width,radius,center):
        width_ = width * size
        radius_ = radius * size
        center_ = center * size + (size-1)/2
        return dict(width_=width_,radius_=radius_,center_=center_)

    def _childrenParamsUpdate(self,radius_,center_):
        for traj in self.centerTraj:
            traj.setParams(radius=radius_,center=center_)

    def _compute(self,size,wrap,width_,intensity,blinkPeriod,dt,blink):
        if self._hidden:
            self._data[...] = 0.0;
        else:
            center = self.getCenter()
            self._data = utils.gaussNd(size,wrap,intensity,width_,center)


        if blink:
            period = int(round(blinkPeriod/dt))
            if period//2  == self._blinkCounter:
                self._hidden = not(self._hidden)
                self._blinkCounter = 0
            else:
                self._blinkCounter += 1



    def getCenter(self):
        return np.array([traj.getData() for traj in self.centerTraj])

    def getShape(self):
            return self.getArg('intensity'),self.getArg('width_')
