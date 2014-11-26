import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.ticker import FuncFormatter
import matplotlib.gridspec as gridspec
"""
    Matplot lib static graphic labrary
    TODO configuration file with dpi, color map, size of plot etc...
"""


def __egaliseColorBar(data,bar):
                maximum = np.amax(data)
                minimum = np.amin(data)
                egal = max(abs(maximum),abs(minimum))
                plt.clim(-egal,+egal)
                bar.set_ticks([__roundUp(-egal),0,__roundDown(+egal)])
                
def __roundDown(x):
        return math.floor(x*100)/100
def __roundUp(x):
        return math.ceil(x*100)/100
def __finalize():
        plt.xticks([])
        plt.yticks([])


def plotArray(data):
        """
            Plot a np.array, with egalised colorbar
        """
        ret = plt.imshow(data,interpolation='nearest',cmap='RdYlBu_r',origin='lower')
        if np.sum(data) != 0:
            bar = plt.colorbar(shrink=.92)
            __egaliseColorBar(data,bar)
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
                        ax = plt.subplot(gs[i/width,i%width :])         
                else:
                        ax = plt.subplot(gs[i/width,i%width])           
                array = name_array_dict[name]
                plotArray(array)
                ax.set_title(name)
                i+=1

        
        
                
        

