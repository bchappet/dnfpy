import numpy as np

from dnfpyUtils.stats.trajectory import Trajectory
class LyapunovMap(Trajectory):
        """
        Input: 
            conv : map (child)
            act : map (child)
            input : map (child)
            fielMap : map (constructor) to get h and th
        Output:
            energy
            As defined in "existence of Lyapunov function for neural field equation as an extensino of lyapunov functino for hopfield model"
            Kubota, Aihara 2004
        """
        def __init__(self,name,fieldMap,dt=0.1,**kwargs):
                super(LyapunovMap,self).__init__(name=name,dt=dt,**kwargs)
                self.field = fieldMap


        def _compute(self,conv,act,input):
                dx = 0.01 #TODO check
                h = self.field.getArg('h')
                th = self.field.getArg('th')
                if np.sum(act) > 0:
                    energy = -1/2*np.sum(act*conv)*dx - np.sum((input - th + h)*act)*dx
                else:
                    energy = np.nan

                self._data = energy
                self.trace.append(self._data)

        




