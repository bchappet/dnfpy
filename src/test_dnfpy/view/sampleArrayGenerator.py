import numpy as np
import scipy.signal as signal



"""
    Provide utility methods for the graphical tests
"""


def getGaussian2D(size,std):
        x = signal.gaussian(size,std)
        y = x.reshape((size,1))
        x = x.reshape((1,size))
        return x*y

def getDOG2D(size):
        a = getGaussian2D(size,size/4.) * 1.4
        b = getGaussian2D(size,size/1.)
        return a - b

def getGradient(size,incresing):
    if incresing:
        a = np.linspace(-1,1,size)
    else:
        a = np.linspace(1,-1,size)
    x = np.zeros((size,size))
    for i in range(size):
        x[:,i] = a
    return x


def getRandomMarquedArray(size):
    val = 1
    a = np.random.rand(size,size)*2*val - val 
    for i in range(size):
         a[i][i] = val
         a[i][size-1-i] = -val
         a[0][i] = val
         a[size-1][i] = -val
         a[i][0] = val
         a[i][size-1] = val
    return a

