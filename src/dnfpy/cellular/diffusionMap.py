from dnfpy.core.mapND import MapND
import numpy as np
import cv2


def laplacian(source,dim,wrap):

    if dim == 2:
        border = cv2.BORDER_WRAP if wrap else cv2.BORDER_DEFAULT
        X = cv2.copyMakeBorder(source,1,1,1,1,borderType=border)
        return X[0:-2,1:-1]+X[2:,1:-1]+X[1:-1,2:]+X[1:-1,0:-2]-4*X[1:-1,1:-1]
    elif dim == 1:
        if wrap:
            X = np.concatenate(([source[-1]],source,[source[0]]))
        else :
            X = np.concatenate(([0],source,[0]))
        return X[0:-2]+X[2:]-2*X[1:-1]





    



class DiffusionMap(MapND):
        """
        Diffusion equation
        D is the diffusion constant
        
        """
        def __init__(self,name,size,dim,dt=0.1,D=1.0,tau=0.1,wrap=True,leak=0.101,
                     **kwargs):
            super().__init__(name=name,size=size,dim=dim,dt=dt,wrap=wrap,D=D,tau=tau,leak=leak,
                                           **kwargs)
            
        def _compute(self,dt,tau,D,wrap,act,leak,dim):
                self._data += dt/tau * D * laplacian(self._data,dim,wrap) + 0.1*act -0.1*leak*self._data


