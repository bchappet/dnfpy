import numpy as np
from cffi import FFI

ffi = FFI()
ffi.cdef("""
    void initSimu(int width,int height,char* cellName,char* connecterName);

    void step();
    void nstep(int n);
    void synch();

    void getArrayInt(int index,int* array);
    void getArrayBool(int index,bool * array);
    void getArrayFloat(int index,float * array);

    void setArrayInt(int index, int* array);
    void setArrayBool(int index, bool* array);
    void setArrayFloat(int index, float* array);

    void setCellInt(int x,int y,int index,int val);
    void setCellBool(int x,int y,int index,bool val);
    void setCellFloat(int x,int y,int index,float val);
""")


size=13
C = ffi.dlopen("./libhardsimu.so")

C.initSimu(size,size,"cellrsdnf","rsdnfconnecter")
res = np.ones((size,size),dtype=np.intc)
#res = np.ascontiguousarray(res, dtype=np.intc)
print res
C.getArrayInt(0,ffi.cast("int *",res.ctypes.data))
print res
C.setCellInt(0,0,0,10)
C.setCellBool(0,0,1,True)
C.synch()
C.getArrayInt(0,ffi.cast("int *",res.ctypes.data))
print res
C.step()
C.getArrayInt(0,ffi.cast("int *",res.ctypes.data))
print res
for i in range(20):
    C.step()
    C.getArrayInt(0,ffi.cast("int *",res.ctypes.data))
    print res



