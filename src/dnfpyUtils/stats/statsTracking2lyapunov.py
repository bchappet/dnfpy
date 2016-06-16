from dnfpyUtils.stats.statsTracking2 import StatsTracking2
from dnfpyUtils.stats.lyapunovMap import LyapunovMap
from dnfpyUtils.stats.movingAverage import MovingAverage
from dnfpyUtils.stats.derivative import Derivative

class StatsTracking2lyapunov(StatsTracking2):
    def initMaps(self,size,dim,dt=0.1,wrap=True,mapUnderStats="",**kwargs):
        computeLi = super().initMaps(size,dim,dt,wrap,mapUnderStats,**kwargs)

        fieldMap = self.runner.getMap("Potential"+mapUnderStats)
        self.lyapunov = LyapunovMap("Lyapunov",dt=dt,fieldMap=fieldMap)
        self.lyapunovMA = MovingAverage("LyapunovMA",dt=dt,windowSize=1.)
        self.lyapunovMA.addChildren(data=self.lyapunov)
        self.lyapunovDerivative = Derivative("LyapunovDerivative",dt=dt)
        self.lyapunovDerivative.addChildren(data=self.lyapunovMA)
        computeLi .append(self.lyapunovDerivative)

        return computeLi


    def getArrays(self):
        li =  super().getArrays()
        li.extend([self.lyapunovDerivative,self.lyapunovMA])
        return li
