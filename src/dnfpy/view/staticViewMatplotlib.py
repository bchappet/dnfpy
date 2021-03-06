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
        bar.set_ticks([-egal,0,+egal])
        #bar.set_ticks_label([__roundUp(-egal),0,__roundDown(+egal)])
    except Exception as e:
        print("Warning : ", e)

def __roundDown(x):
        #return math.floor(x*PRECISION)//PRECISION
        return round(x,3)

def __roundUp(x):
        #return math.ceil(x*PRECISION)//PRECISION
        return round(x,3)

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

def plot(data):
    """
    One dimentional field
    """
    ret = plt.plot(data)
    return ret


def plotArrays(name_array_dict,sameBar = False):
        """
        Expect a dictionary {name->array}
        If sameBar then only one color bar is displayed    
        """
        i = 0
        size = len(name_array_dict)
        width = int(math.ceil(math.sqrt(size)))
        height = int(math.ceil(size/float(width)))
        f, axarr = plt.subplots(height,width)
        gs = gridspec.GridSpec(height, width)

        if sameBar:
            egal = 0
            showBar = False
            for name in name_array_dict:
                newEgal = getEgal(name_array_dict[name] )
                if newEgal > egal:
                    egal = newEgal

        else:
            egal = None
            showBar = True
            
        for name in name_array_dict:
                if( i == size-1): #last fig
                        ax = plt.subplot(gs[i//width,i%width :])
                else:
                        ax = plt.subplot(gs[i//width,i%width])
                array = name_array_dict[name]
                if len(array.shape) < 3:
                    plotArray(array,egal=egal,showBar=showBar)
                else:
                    ax.imshow(array)
                ax.set_title(name)
                i+=1
        if sameBar:
            bar = plt.colorbar(shrink=.92)
            egaliseColorBar(egal,bar)


def show():
    plt.show()





