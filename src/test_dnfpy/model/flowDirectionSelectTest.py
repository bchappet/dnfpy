import numpy as np
from dnfpy.core.map2D import Map2D
import cv2
import dnfpy.core.utils as utils
import math
from dnfpy.core.funcMap2D import FuncMap2D


size=20
dt=0.1
cX = 3
cY = 7
kernel = FuncMap2D(utils.gauss2d,"gauss",size,dt=dt,centerX=cX,centerY=cY,wrap=True,
                intensity=1.,width=10)
kernel.compute()

kdata = kernel.getData()
max = np.max(kdata)
itemIndex = np.where(kdata==max)
print itemIndex
cx = itemIndex[1][0]
cy = itemIndex[0][0]

assert(cx==cX)
assert(cy==cY)








