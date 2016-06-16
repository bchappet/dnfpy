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
        def __init__(self,name,dt=0.1,fieldMap=None,**kwargs):
                super(LyapunovMap,self).__init__(name=name,dt=dt,**kwargs)
                self.field = fieldMap


        def _compute(self):
                dx = 1/self.field.getArg('size')
                h = self.field.getArg('h')
                th = self.field.getArg('th')
                act = self.field.getActivation().getData()
                input = self.field.getChild('aff').getData()
                conv = self.field.getChild('lat').getData()
                        

                if np.sum(act) > 0:
                    energy = -1/2*np.sum(act*conv)*dx - np.sum((input - th + h)*act)*dx
                else:
                    energy = np.nan

                self._data = energy
                self.trace.append(self._data)

        




