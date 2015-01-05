import numpy as np
from ctypes import *
import numpy.ctypeslib as npct
libac = npct.load_library("libac", "lib/")

PP_UBYTE = POINTER(POINTER(c_ubyte))
CELL_FUNC = CFUNCTYPE(None, PP_UBYTE, PP_UBYTE)
cell_fun_c = libac.compute_cell_rsdnf
cell_fun_c.argtypes = [PP_UBYTE,PP_UBYTE]

def cell_func_py(data,neighs):
    cell_fun_c(data,neighs)

cell_fun = CELL_FUNC(cell_func_py)

if __name__ == "__main__":
        size = 20
        depth = 5
        buffs = [ np.zeros((size,size,depth),dtype=np.uint8),
                 np.zeros((size,size,depth),dtype=np.uint8)]
        current = 0
        fun = libac.synchronous_step_neumann
        N = 10



        buffs[current][size/2,size/2,1] = N
        buffs[current][size/2,size/2,2] = N
        buffs[current][size/2,size/2,3] = N
        buffs[current][size/2,size/2,4] = N
        print("Before")
        print(buffs[current][:,:,0])
        fun.argtypes = [
                        np.ctypeslib.ndpointer(dtype=np.uint8,ndim=3,flags='C_CONTIGUOUS'),
                        np.ctypeslib.ndpointer(dtype=np.uint8,ndim=3,flags='C_CONTIGUOUS'),
                        c_int,c_int,c_int,CELL_FUNC]
        for i in range(10):
            nextB = (current+1) % 2
            print("nextB %s"%nextB)
            fun(buffs[current],buffs[nextB],size,size,depth,cell_fun)
            result = buffs[nextB]
            current = nextB
            print("After")
            print(result[:,:,0])
            print(np.sum(result))
