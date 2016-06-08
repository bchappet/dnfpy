import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.ticker import FuncFormatter
import matplotlib.gridspec as gridspec
"""
    Matplot lib static graphic labrary
    TODO configuration file with dpi, color map, size of plot etc...
"""

PRECISION = 10000000
def egaliseColorBar(egal,bar):
    try:
        bar.set_ticks([__roundUp(-egal),0,__roundDown(+egal)])
    except Exception as e:
        print("Warning : ", e)

def __roundDown(x):
        return math.floor(x*PRECISION)//PRECISION
def __roundUp(x):
        return math.ceil(x*PRECISION)//PRECISION
def __finalize():
        plt.xticks([])
        plt.yticks([])

def getEgal(data):
        """
        Return max(abs(min),abs(max))
        """
        maximum = np.amax(data)
        minimum = np.amin(data)
        egal = max(abs(maximum),abs(minimum))
        if egal == 0:
                egal = 1
        return egal

def plotArray(data,showBar=True,egal=None):
        """
            Plot a np.array, with egalised colorbar
        """
        if not(egal):
            egal = getEgal(data)

        ret = plt.imshow(data,interpolation='nearest',cmap='RdYlBu_r',vmin=-egal,vmax=+egal)
        if showBar  and np.sum(data) != 0:
            bar = plt.colorbar(shrink=.92)
            egaliseColorBar(egal,bar)
        __finalize()
        return ret


def plotArrays(name_array_dict):
        """Expect a dictionary {name->array}"""
        i = 0
        size = len(name_array_dict)
        width = int(math.ceil(math.sqrt(size)))
        height = int(math.ceil(size/float(width)))
        f, axarr = plt.subplots(height,width)
        gs = gridspec.GridSpec(height, width)
        for name in name_array_dict:
                if( i == size-1): #last fig
                        ax = plt.subplot(gs[i//width,i%width :])
                else:
                        ax = plt.subplot(gs[i//width,i%width])
                array = name_array_dict[name]
                if len(array.shape) < 3:
                    plotArray(array)
                else:
                    ax.imshow(array)
                ax.set_title(name)
                i+=1

def show():
    plt.show()





