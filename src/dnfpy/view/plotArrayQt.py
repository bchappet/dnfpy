import numpy as np
import qimage2ndarray #http://kogs-www.informatik.uni-hamburg.de/~meine/software/qimage2ndarray/doc/#converting-ndarrays-into-qimages
import json

def __getColorMap(nameCm='RdYlBu_r'):
        folder = 'stylesheet/'
        f = file(folder+nameCm+'.cm','r')
        array = json.load(f)
        return array


__cm = __getColorMap()



def npToQImage(array):
        """
                Transform the array into a qImage with color map
                return QImage
        """
        if len(array.shape) == 3 and array.shape[2] == 3:
                qImage = qimage2ndarray.array2qimage(array).rgbSwapped()
        else:
            if len(array.shape) == 3:
                array = array[...,0]
            max_a = max(abs(np.min(array)),np.max(array))
            qImage = qimage2ndarray.gray2qimage(array,(-max_a,max_a))
            qImage.setColorTable(__cm)




        return qImage

