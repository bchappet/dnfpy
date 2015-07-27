import numpy as np
import cv2

def compute(data):
    """
    !python main.py ModelCellular 512 0.3 "{'comp':'gameOfLife'}"
    """
    wrap = False
    if wrap:
            X = cv2.copyMakeBorder(data,1,1,1,1,cv2.BORDER_WRAP)
    else:
            X = cv2.copyMakeBorder(data,1,1,1,1,cv2.BORDER_CONSTANT,0)
    # Count neighbors
    N = (X[0:-2,0:-2] + X[0:-2,1:-1] + X[0:-2,2:] +
         X[1:-1,0:-2]                + X[1:-1,2:] +
         X[2:  ,0:-2] + X[2:  ,1:-1] + X[2:  ,2:])

    # Apply rules
    birth = (N==3) & (X[1:-1,1:-1]==0)
    survive = ((N==2) | (N==3)) & (X[1:-1,1:-1]==1)
    X[...] = 0
    x = X[1:-1,1:-1]
    x[birth | survive] = 1
    return x


def initModel():
    return np.random.randint(0,2,(size,size))

