import numpy as np

from dnfpy.core.mapND import MapND
class LyapunovMap(MapND):
        """
        Input: 
            conv : map (child)
            act : map (child)
            input : map (child)
            h : float rest potential (constructor)
            th : float threshold (constructor)
        Output:
            energy
            As defined in "existence of Lyapunov function for neural field equation as an extensino of lyapunov functino for hopfield model"
            Kubota, Aihara 2004
        """
        def __init__(self,name,size=0,h=0,th=0.64,dim=0,dt=0.1,**kwargs):
                super(LyapunovMap,self).__init__(name=name,size=size,dim=dim,dt=dt,h=h,th=th,**kwargs)
                self.meanErrorSave = []
                self.setArg(mean=0.0)


        def _compute(self,conv,act,input,h,th):
                dx = 0.01 #TODO check
                energy = -1/2*np.sum(act*conv)*dx - np.sum((input - th + h)*act)*dx
                self._data = energy
                self.meanErrorSave.append(energy)
                self.setArg(mean=np.mean(self.meanErrorSave))





