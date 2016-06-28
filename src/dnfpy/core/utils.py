import cv2
import scipy.ndimage.filters as filter
import numpy as np
import scipy.signal as signal
from scipy.special import erf
import copy
import sys
#import numba


#Utilitary functions
#TODO try with cython

#@numba.autojit
def generateWrappedDistance(size,center,wrap):
    """Compute the oriented distance (real) between the set (0..size-1) and the center
    if wrap is true, the distance will be the minimal from center and center + size"""
    distI = []
    Xi = [np.arange(0, size, 1,dtype= np.float32),]
    center = np.array(center)
    for i in range(len(center)):
        Xi.append(Xi[i][:,np.newaxis]) #no way it's working for dim >2 TODO

    if wrap:
        for i in range(len(center)):
            center[i] %= size
            distI.append(Xi[i]-center[i])
        for i in range(len(center)):
            cas1 = abs(Xi[i] - (center[i] + size)) < abs(Xi[i]-center[i])
            cas2 = abs(Xi[i] - (center[i] - size)) < abs(Xi[i]-center[i])
        
            distI[i][cas1] = (Xi[i] - (center[i] + size))[cas1]
            distI[i][cas2] = (Xi[i] - (center[i] - size))[cas2]

            #distI[i] = np.minimum(distI[i],abs(Xi[i]-(center[i]+size)))
            #distI[i] = np.minimum(distI[i],abs(Xi[i]-(center[i]-size)))
    else:
        for i in range(len(center)):
            distI.append(abs(Xi[i]-(center[i])))

    return distI
    

def wrappedVector(z0,z,size):
        """
        Generate the wrapped vector z0 - z
        If a nan is in z0 or z, return nan
        """
        if np.any(np.isnan(z0)) or np.any(np.isnan(z)):
                return np.ones_like(z)*np.nan

        z0 = z0 % size
        z = z % size
        dist = z0-z

        cas1 = abs(z0 - (z + size)) < abs(z0-z)
        cas2 = abs(z0 - (z - size)) < abs(z0-z)

        dist[cas1] = (z0 - (z + size))[cas1]
        dist[cas2] = (z0 - (z - size))[cas2]
        return dist

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
    if width <= 0 :
        return np.zeros((size,)*dim)
    distI = generateWrappedDistance(size,center,wrap);
    sumDistSquared = np.zeros((size,)*dim)
    for dist in distI:
            sumDistSquared += dist**2
    return intensity * np.exp( -( sumDistSquared) / (width**2))

def gaussFix(size,wrap,intensity,width,center):
    dim = len(center) #nb Dim
    distI = generateWrappedDistance(size,center,wrap);
    sumDistSquared = np.zeros((size,)*dim)
    for dist in distI:
            sumDistSquared += dist**2
    return intensity * np.exp(-sumDistSquared/(2.0 * width**2))

def pos_part_s(x):
    if(x >= 0):
        return x
    else:
        return 0
pos_part = np.vectorize(pos_part_s, otypes=[np.float]) 

def weightsFix(space,lat,k,w):
    x = space[0]
    
    if(lat == 'dog'):
        y = k * np.exp(-x**2/(2.0 * w**2))
    if(lat == 'doe'):
        y = k * np.exp(-4.0 * np.fabs(x)/(w**2))
    elif(lat == 'dol'):
        y = k * pos_part(1.0 - np.fabs(x)/(2.0 * w)) 
    elif(lat == 'step'):
        y = k * np.piecewise(x, [np.fabs(x) < w], [1])

    return y


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
    if proba <= 0 :
        return np.zeros((size,)*dim)
    distI = generateWrappedDistance(size,center,wrap);
    sumDistSquared = np.zeros((size,)*dim)
    for dist in distI:
            sumDistSquared += abs(dist)
    return intensity * (proba ** (sumDistSquared ) )


def expFix(size,wrap,intensity,proba,center):
    """Make an Exponential kernel """
    w = proba
    k = intensity
    dim = len(center) #nb Dim
    distI = generateWrappedDistance(size,center,wrap);
    sumDistSquared = np.zeros((size,)*dim)
    for dist in distI:
            sumDistSquared += dist

    return k * np.exp(-4.0 * np.fabs(sumDistSquared)/(w**2))




def linNd(size,wrap,alpha,beta,center):
    """Make an linear kernel """
    distX = generateWrappedDistance(size,center,wrap);
    print("alpha :",alpha," beta ",beta)
    return np.maximum(-alpha*(np.fabs(distX)) + beta,0)

def stepNd(size,wrap,intensity,width,center):
    dim = len(center) #nb Dim
    if width <= 0 :
        return np.zeros((size,)*dim)
    distI = generateWrappedDistance(size,center,wrap);
    sumDistSquared = np.zeros((size,)*dim)
    for dist in distI:
            sumDistSquared += np.abs(dist)
 
    return np.where(sumDistSquared > width , 0,intensity)
    


def cosTraj(time,center,radius,period,phase):
    """Definie a cosinus trajectory"""
    return center + radius * np.cos(2*np.pi*(time/period-phase))

def affTraj(wrapSize,wrap,time,speed,origin):
    """Return a affine traj: a * time + b"""
    pos =  speed * time + origin
    return pos


def sumArrays(varlist):
    """Sum n arrays"""
    res = 0
    for i in range(len(varlist)):
        res = np.add(res, varlist[i])

    return res

def weightedSumArrays(maplist,argList):
    res = 0
   # print(varlist)
   # print("======================================")
    for data,w in zip(maplist,argList):
        res = np.add(res, data*w)

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


def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n



def gaussSolution(x,k,w):
    return np.sqrt(np.pi)/2 * k * w *erf(x/w)


def dogSolution(x,kE,kI,wE,wI):
    return gaussSolution(x,kE,wE) - gaussSolution(x,kI,wI)

def convolve(source,kernel,wrap=True):
    dim = len(source.shape)
    if wrap:
        kshape = kernel.shape[0]
        minKS = 10
        if kshape < minKS:
            #extend matrice to 5x5 minimum
            ks2 = (kshape-1)//2
            mks2 = (minKS-1)//2
            kernel = cv2.copyMakeBorder(kernel,minKS-ks2,minKS-ks2,minKS-ks2,minKS-ks2,cv2.BORDER_CONSTANT,0.0)

    if dim == 2:
        border = cv2.BORDER_WRAP if wrap else cv2.BORDER_CONSTANT
        return cv2.filter2D(source,-1,cv2.flip(kernel,-1),anchor=(-1,-1),borderType=border)
    elif dim == 1:
        border = 'wrap' if wrap else 'reflect'
        return filter.convolve(source,kernel,mode=border)
    else:
        raise Exception("Dim ",dim, " is not supported")

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    size = 21
    center = (size //2,size//2)
    exp = expNd(size=size,wrap=True,intensity=1,proba=0.98,center=center)
    plt.imshow(exp)
    plt.show()

