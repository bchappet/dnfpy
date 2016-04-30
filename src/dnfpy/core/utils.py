import numpy as np
import sys
import scipy.signal as signal
import copy
#import numba


#Utilitary functions
#TODO try with cython

#@numba.autojit
def generateWrappedDistance(size,centerX,centerY,wrap):
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
    (distX,distY) = generateWrappedDistance(size,centerX,centerY,wrap);
    return intensity * np.exp( (-((distX)**2 + (distY)**2)) / width**2)

def exp2d(size,wrap,intensity,proba,centerX,centerY):
    """Make an Exponential kernel """
    (distX,distY) = generateWrappedDistance(size,centerX,centerY,wrap);
    return intensity * (proba ** (distX + distY) )

def lin2d(size,wrap,alpha,beta,centerX,centerY):
    """Make an linear kernel """
    (distX,distY) = generateWrappedDistance(size,centerX,centerY,wrap);
    return beta*np.maximum(0,alpha-(distX+distY))



def cosTraj(time,center,radius,period,phase):
    """Definie a cosinus trajectory"""
    return center + radius * np.cos(2*np.pi*(time/period-phase))

def affTraj(wrapSize,wrap,time,speed,origin):
    """Return a affine traj: a * time + b"""
    pos =  speed * time + origin
    if wrap:
        pos = pos % wrapSize
    return pos


def sumArrays(varlist):
    """Sum n arrays"""
    res = 0
    for i in range(len(varlist)):
        res = np.add(res, varlist[i])

    return res

def weightedSumArrays(varlist):
    res = 0
   # print(varlist)
   # print("======================================")
    for i in range(0,len(varlist),2):
        res = np.add(res, varlist[i]*varlist[i+1])

    return res




def sumImageArrays(varlist):
    """Sum n arrays to each color component of an image"""
    k=len(varlist)
    for i in range(len(varlist)):
        if len(varlist[i].shape)==3:
            k = i
    im = copy.copy(varlist[k])
    perturb = 0
    for i in range(len(varlist)):
        if i!=k:
            perturb = perturb + varlist[i]
    im[:,:,0] = perturbe(im[:,:,0], perturb)
    im[:,:,1] = perturbe(im[:,:,1], perturb)
    im[:,:,2] = perturbe(im[:,:,2], perturb)

    return im

def perturbe(pixels,perturb):
    """pixel_modif = perturbe * (255-pixel) + (1-perturbe) * pixel"""
    # normalisation perturbation
    perturb = np.abs(perturb)
    perturb = np.minimum(perturb,1)
    return np.add(np.multiply(perturb,255-pixels),np.multiply(1-perturb,pixels))

def subArrays(a,b):
    """Return a - b"""
    return a-b

def getAssymetricGaussian2D(size,intXY,stdXY):
    x = signal.gaussian(size,stdXY[0]) * intXY[0]
    y = signal.gaussian(size,stdXY[1]) * intXY[1]

    x = x.reshape((1,size))
    y = y.reshape((size,1))
    return np.dot(y,x)

def abs(x):
        return np.abs(x)

def discretize(array,nbStep):
    """
    return a discrete version of the array with nbStep discretization steps
    """
    shape = array.shape
    min = array.min()
    max = array.max()
    step = abs(max-min)/nbStep + 1e-8
    values = np.arange(min+step/2,max+step/2,step)
    bins = np.arange(min,max+step,step)
    arrBins = np.digitize(array.flatten(),bins) - 1
    resFlat =  values[arrBins]
    return resFlat.reshape(shape)

def matrixTranslation(array,tx,ty):
    import cv2
    rows,cols = array.shape
    M = np.float32([[1,0,tx],[0,1,ty]])
    return cv2.warpAffine(array,M,(cols,rows))


def conv2(a, b):
    '''
    Computes the circular convolution of the (real-valued) matrices a and b.
    '''
    return np.fft.ifftshift(np.fft.ifft2(np.fft.fft2(a) * np.fft.fft2(b))).real
