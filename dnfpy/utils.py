import numpy as np


#Utilitary functions 
#TODO try with cython


def __generateWrappedDistance(size,centerX,centerY,wrap):
    """Compute the distance (real) between the set (0..size-1) and the center
    if wrap is true, the distance will be the minimal from center and center + size"""
    X = np.arange(0, size, 1,dtype= np.float32)
    Y = X[:,np.newaxis]
    distX = abs(X-centerX)
    distY = abs(Y-centerY)
     
    if wrap:
            distX = np.minimum(distX,abs(X-(centerX+size)))
            distY = np.minimum(distY,abs(Y-(centerY+size)))
    return (distX,distY)


def gauss2d(size,wrap,intensity,width,centerX,centerY):
    """ Make a  gaussian kernel."""
    (distX,distY) = __generateWrappedDistance(size,centerX,centerY,wrap);
    return intensity * np.exp( (-((distX)**2 + (distY)**2)) / width**2)

def exp2d(size,wrap,intensity,proba,centerX,centerY):
    """Make an Exponential kernel """
    (distX,distY) = __generateWrappedDistance(size,centerX,centerY,wrap);
    return intensity * (proba ** (distX + distY) )

def cosTraj(time,center,radius,period,phase):
    """Definie a cosinus trajectory"""
    return center + radius * np.cos(2*np.pi*(time/period-phase))
