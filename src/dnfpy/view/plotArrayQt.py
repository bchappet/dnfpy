import numpy as np
import qimage2ndarray #http://kogs-www.informatik.uni-hamburg.de/~meine/software/qimage2ndarray/doc/#converting-ndarrays-into-qimages
import json

def getColorMap(nameCm='RdYlBu_r'):
        folder = 'stylesheet/'
        f = file(folder+nameCm+'.cm','r')
        array = json.load(f)
        return array


__cm = getColorMap()


def npToQImage(array):
        min_ = np.min(array)
        max_ = np.max(array)
        return npToQImage2(array,min_,max_)


def npToQImage2(array,minArray,maxArray):
        """
                Transform the array into a qImage with color map
                return QImage
        """
        if len(array.shape) == 3 and array.shape[2] == 3:
                qImage = qimage2ndarray.array2qimage(array).rgbSwapped()
        else:
            if minArray == maxArray:
                max_a = 10e-10
            else:
                max_a = max(abs(minArray),abs(maxArray))
            qImage = qimage2ndarray.gray2qimage(array,(-max_a,max_a))
            qImage.setColorTable(__cm)

        return qImage
