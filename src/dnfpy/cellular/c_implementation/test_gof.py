import numpy as np
from ctypes import *
import numpy.ctypeslib as npct
libac = npct.load_library("libac", "lib/")

class CellArgs(Structure):
    _fields_ = []

PP_UBYTE = POINTER(POINTER(c_ubyte))
CELL_FUNC = CFUNCTYPE(None, PP_UBYTE, PP_UBYTE,CellArgs)
cell_fun_c = libac.compute_cell_gof
cell_fun_c.argtypes = [PP_UBYTE,PP_UBYTE,CellArgs]

def game_life_func(data,neighs,args):
    cell_fun_c(data,neighs,args)

cell_fun = CELL_FUNC(game_life_func)

if __name__ == "__main__":
        size = 10
        buffs = [ np.zeros((size,size,1),dtype=np.uint8),
                 np.zeros((size,size,1),dtype=np.uint8)]
        current = 0
        fun = libac.synchronous_step_moore


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
                        c_int,c_int,c_int,CELL_FUNC,CellArgs]
        for i in range(10):
            nextB = (current+1) % 2
            print("nextB %s"%nextB)
            fun(buffs[current],buffs[nextB],size,size,1,cell_fun,CellArgs())
            result = buffs[nextB]
            current = nextB
            print("After")
            print(result.reshape(size,size))
            print(np.sum(result))
