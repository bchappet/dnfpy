import numpy as np
import scipy.signal as signal
import copy
import sys
#import numba


#Utilitary functions
#TODO try with cython

#@numba.autojit
def generateWrappedDistance(size,center,wrap):
    """Compute the distance (real) between the set (0..size-1) and the center
    if wrap is true, the distance will be the minimal from center and center + size"""
    distI = []
    Xi = [np.arange(0, size, 1,dtype= np.float32),]
    for i in range(len(center)):
        distI.append(abs(Xi[i]-center[i]))
        Xi.append(Xi[i][:,np.newaxis]) #no way it's working for dim >2 TODO

    if wrap:
        for i in range(len(center)):
            distI[i] = np.minimum(distI[i],abs(Xi[i]-(center[i]+size)))
    return distI

def generateWrappedDistance2(size,res,centerX,wrap):
    """Compute the distance (real) between the set (0..size-1) and the center
    if wrap is true, the distance will be the minimal from center and center + size"""
    X = np.linspace(0, size, res,dtype= np.float32)
    distX = abs(X-centerX)

    if wrap:
            distX = np.minimum(distX,abs(X-(centerX+size)))
    return distX



def gaussNd(size,wrap,intensity,width,center):
    """ Make a  gaussian kernel."""
    dim = len(center) #nb Dim
    distI = generateWrappedDistance(size,center,wrap);
    sumDistSquared = np.zeros((size,)*dim)
    for dist in distI:
            sumDistSquared += dist**2
    return intensity * np.exp( -( sumDistSquared) / (width**2))

def gaussian(x,intensity,width):
    """Gaussian kernel V2"""
    return intensity/(width*np.sqrt(np.pi))*np.exp(-x**2/(2*width**2))

def gaussianNd(size,res,wrap,intensity,width,center):
    """
    width is in the size referential width \in [0,size]
    """
    distX = generateWrappedDistance2(size,res,center,wrap);
    return gaussian(distX,intensity,width)



def expNd(size,wrap,intensity,proba,center):
    """Make an Exponential kernel """
    dim = len(center) #nb Dim
    distI = generateWrappedDistance(size,center,wrap);
    sumDistSquared = np.zeros((size,)*dim)
    for dist in distI:
            sumDistSquared += dist
    return intensity * (proba ** (sumDistSquared ) )

def linNd(size,wrap,alpha,beta,center):
    """Make an linear kernel """
    distX = generateWrappedDistance(size,center,wrap);
    return np.clip(-alpha*(distX) + beta,0,sys.float_info.max)


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

def getAssymetricGaussianND(size,int,std):
    x = signal.gaussian(size,std) * int

    x = x.reshape((1,size))
    return x

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


