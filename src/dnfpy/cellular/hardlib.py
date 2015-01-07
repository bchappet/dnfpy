import numpy as np
from cffi import FFI

ffi = FFI()
ffi.cdef("""
    void initSimu(int width,int height,char* cellName,char* connecterName);

    void step();
    void nstep(int n);
    void synch();

    void setMapParamInt(int index,int value,char* path);
    void setMapParamBool(int index,bool value,char* path);
    void setMapParamFloat(int index,float value,char* path);

    void getCellAttribute(int x,int y,int index,void* value);
    void setCellAttribute(int x,int y,int index, void* value);

    void getArrayAttributeInt(int index, int* array);
    void getArrayAttributeBool(int index, bool* array);
    void getArrayAttributeFloat(int index, float* array);

    void setArrayAttributeInt(int index, int* array);
    void setArrayAttributeBool(int index, bool* array);
    void setArrayAttributeFloat(int index, float* array);


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



class HardLib:
    def __init__(self,sizeX,sizeY,cellType,connecterType):
        self.C = ffi.dlopen("./cpp_implementation/libhardsimu.so")
        self.C.initSimu(sizeX,sizeY,cellType,connecterType)

    def synch(self):
        self.C.synch();

    def step(self):
        self.C.step();

    def nstep(self,n):
        self.C.nstep();

    def setMapParams(self,idParam,val,path="."):
        dtype = type(val)
        if dtype == int:
            self.C.setMapParamInt(idParam,val,path)
        elif dtype == bool:
            self.C.setMapParamBool(idParam,val,path)
        elif dtype == float:
            self.C.setMapParamFloat(idParam,val,path)
        else:
            raise AttributeError("Expecting int bool or float as dtype")


    def setCellAttribute(self,x,y,idAttribute,val):
        dtype = type(val)
        if dtype == int:
            point = ffi.new("int *",val)
        elif dtype == bool:
            point = ffi.new("bool *",val)
        elif dtype == float:
            point = ffi.new("float *",val)
        else:
            raise AttributeError("Expecting int bool or float as dtype")

        self.C.setCellAttribute(x,y,idAttribute,point)

    def setArrayAttribute(self,idAttribute,npArray):
        dtype = npArray.dtype
        if dtype == np.intc:
            self.C.setArrayAttributeInt(0,ffi.cast("int *",npArray.ctypes.data))
        elif dtype == np.float:
            self.C.setArrayAttributeFloat(0,ffi.cast("float *",npArray.ctypes.data))
        elif dtype == np.bool:
            self.C.setArrayAttributeBool(0,ffi.cast("bool *",npArray.ctypes.data))
        else:
            raise AttributeError("Expecting int bool or float as dtype")

    def getArrayAttribute(self,idAttribute,npArray):
        dtype = npArray.dtype
        if dtype == np.intc:
            self.C.getArrayAttributeInt(0,ffi.cast("int *",npArray.ctypes.data))
        elif dtype == np.float:
            self.C.getArrayAttributeFloat(0,ffi.cast("float *",npArray.ctypes.data))
        elif dtype == np.bool:
            self.C.getArrayAttributeBool(0,ffi.cast("bool *",npArray.ctypes.data))
        else:
            raise AttributeError("Expecting int bool or float as dtype")



    def getCellAttribute(self,x,y,idAttribute,dtype):

        if dtype == int:
            point = ffi.new("int *")
        elif dtype == bool:
            point = ffi.new("bool *")
        elif dtype == float:
            point = ffi.new("float *")
        else:
            raise AttributeError("Expecting int bool or float as dtype")
        self.C.getCellAttribute(x,y,idAttribute,point)
        return point[0]

    def setRegCell(self,x,y,regIndex,val):
        ty = type(val)
        if ty == int:
            self.C.setCellInt(x,y,regIndex,val)
        elif ty == bool:
            self.C.setCellBool(x,y,regIndex,val)
        elif ty == float:
            self.C.setCellFloat(x,y,regIndex,val)
        else:
            raise AttributeError("Expecting int bool or float as dtype")



    def getRegArray(self,regIndex,npArray):
        dtype = npArray.dtype
        if dtype == np.intc:
            self.C.getArrayInt(0,ffi.cast("int *",npArray.ctypes.data))
        elif dtype == np.float:
            self.C.getArrayFloat(0,ffi.cast("float *",npArray.ctypes.data))
        elif dtype == np.bool:
            self.C.getArrayBool(0,ffi.cast("bool *",npArray.ctypes.data))
        else:
            raise AttributeError("Expecting int bool or float as dtype")
