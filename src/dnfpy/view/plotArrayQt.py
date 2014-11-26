import numpy as np
import qimage2ndarray #http://kogs-www.informatik.uni-hamburg.de/~meine/software/qimage2ndarray/doc/#converting-ndarrays-into-qimages
import pylab
from PyQt4 import QtGui

def __getColorMap(nameCm='RdYlBu_r'):
    cm=[]
    pylabCm =  pylab.cm.get_cmap(nameCm)
    for i in range(256):
        r,g,b,a =  pylabCm(i)
        qrgb = QtGui.qRgb(round(r*255),round(g*255),round(b*255))
        cm.append(qrgb)
    return cm

__cm = __getColorMap()



def npToQImage(array):
    """
        Transform the array into a qImage with color map
        return QImage
    """
    max_a = max(abs(array.min()),array.max())
    qImage = qimage2ndarray.gray2qimage(array,(-max_a,max_a))
    qImage.setColorTable(__cm)
    return qImage

