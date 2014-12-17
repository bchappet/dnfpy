import numpy as np
from ctypes import *
import ctypes
import numpy.ctypeslib as npct
libac = npct.load_library("libac", "lib/")


class AC(Structure):
        _fields_ = [
                        ("buffers",POINTER(POINTER(c_ubyte))),
                        ("current",c_int),
                        ("n",c_int),
                        ("m",c_int),
                        ("depth",c_int),
                        ("nb_buffer",c_int),
                     ]
        def __init__(self,m,n,depth=1):
                fun = libac.new_cellular_array
                fun.restype = POINTER(AC)
                fun.argtypes = [c_int,c_int]
                self.ac = fun(m,n)


if __name__ == "__main__":
        size = 10
        ac = AC(size,size,1)
        buffs = [ np.zeros((size,size,1),dtype=np.uint8),
                 np.zeros((size,size,1),dtype=np.uint8)]
        current = 0



        fun = libac.synchronous_step

        buffs[current][5,5] = 1
        buffs[current][5,6] = 1
        buffs[current][5,7] = 1
        buffs[current][6,5] = 1
        buffs[current][6,6] = 1
        buffs[current][6,4] = 1

        buffs[current][1,1] = 1
        print("Before")
        print(buffs[current].reshape(size,size))
        fun.argtypes = [
                        np.ctypeslib.ndpointer(dtype=np.uint8,ndim=3,flags='C_CONTIGUOUS'),
                        np.ctypeslib.ndpointer(dtype=np.uint8,ndim=3,flags='C_CONTIGUOUS'),
                        c_int,c_int,c_int]
        for i in range(10):
            nextB = (current+1) % 2
            print("nextB %s"%nextB)
            fun(buffs[current],buffs[nextB],size,size,1)
            result = buffs[nextB]
            current = nextB
            print("After")
            print(result.reshape(size,size))
            print(np.sum(result))






