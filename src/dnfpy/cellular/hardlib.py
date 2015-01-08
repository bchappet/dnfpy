import numpy as np
from cffi import FFI

ffi = FFI()
ffi.cdef("""
    int initSimu(int width,int height,char* cellName,char* connecterName);
    int useMap(int idMap);

    void step();
    void nstep(int n);
    void synch();
    void reset();

    void setMapParamInt(int index,int value,char* path);
    void setMapParamBool(int index,bool value,char* path);
    void setMapParamFloat(int index,float value,char* path);

    int getMapParamInt(int index,char* path);
    bool getMapParamBool(int index,char* path);
    float getMapParamFloat(int index,char* path);

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
        self.C = ffi.dlopen("libhardsimu.so")
        self.__idMap = self.C.initSimu(sizeX,sizeY,cellType,connecterType)

    def __useMap(self):
        self.C.useMap(self.__idMap)

    def synch(self):
        self.__useMap()
        self.C.synch();

    def step(self):
        self.__useMap()
        self.C.step();

    def nstep(self,n):
        self.__useMap()
        self.C.nstep();

    def reset(self):
        self.__useMap()
        self.C.reset()

    def getMapParam(self,idParam,dtype,path="."):
        self.__useMap()
        if dtype == int:
            return self.C.getMapParamInt(idParam,path)
        elif dtype == bool:
            return self.C.getMapParamBool(idParam,path)
        elif dtype == float:
            return self.C.getMapParamFloat(idParam,path)
        else:
            raise AttributeError("Expecting int bool or float as dtype. Was %s"%dtype)




    def setMapParam(self,idParam,val,path="."):
        self.__useMap()
        dtype = type(val)
        if dtype == int:
            self.C.setMapParamInt(idParam,val,path)
        elif dtype == bool:
            self.C.setMapParamBool(idParam,val,path)
        elif dtype == float:
            self.C.setMapParamFloat(idParam,val,path)
        else:
            raise AttributeError("Expecting int bool or float as dtype. Was %s"%dtype)


    def setCellAttribute(self,x,y,idAttribute,val):
        self.__useMap()
        dtype = type(val)
        if dtype == int:
            point = ffi.new("int *",val)
        elif dtype == bool:
            point = ffi.new("bool *",val)
        elif dtype == float:
            point = ffi.new("float *",val)
        else:
            raise AttributeError("Expecting int bool or float as dtype. Was %s"%dtype)

        self.C.setCellAttribute(x,y,idAttribute,point)

    def setArrayAttribute(self,idAttribute,npArray):
        self.__useMap()
        dtype = npArray.dtype
        if dtype == np.intc:
            self.C.setArrayAttributeInt(idAttribute,ffi.cast("int *",npArray.ctypes.data))
        elif dtype == np.float:
            self.C.setArrayAttributeFloat(idAttribute,ffi.cast("float *",npArray.ctypes.data))
        elif dtype == np.bool:
            self.C.setArrayAttributeBool(idAttribute,ffi.cast("bool *",npArray.ctypes.data))
        else:
            raise AttributeError("Expecting int bool or float as dtype. Was %s"%dtype)

    def getArrayAttribute(self,idAttribute,npArray):
        self.__useMap()
        dtype = npArray.dtype
        if dtype == np.intc:
            self.C.getArrayAttributeInt(idAttribute,ffi.cast("int *",npArray.ctypes.data))
        elif dtype == np.float:
            self.C.getArrayAttributeFloat(idAttribute,ffi.cast("float *",npArray.ctypes.data))
        elif dtype == np.bool:
            self.C.getArrayAttributeBool(idAttribute,ffi.cast("bool *",npArray.ctypes.data))
        else:
            raise AttributeError("Expecting int bool or float as dtype. Was %s"%dtype)



    def getCellAttribute(self,x,y,idAttribute,dtype):
        self.__useMap()
        if dtype == int:
            point = ffi.new("int *")
        elif dtype == bool:
            point = ffi.new("bool *")
        elif dtype == float:
            point = ffi.new("float *")
        else:
            raise AttributeError("Expecting int bool or float as dtype. Was %s"%dtype)
        self.C.getCellAttribute(x,y,idAttribute,point)
        return point[0]

    def setRegCell(self,x,y,regIndex,val):
        self.__useMap()
        ty = type(val)
        if ty == int:
            self.C.setCellInt(x,y,regIndex,val)
        elif ty == bool:
            self.C.setCellBool(x,y,regIndex,val)
        elif ty == float:
            self.C.setCellFloat(x,y,regIndex,val)
        else:
            raise AttributeError("Expecting int bool or float as dtype. Was %s"%dtype)



    def getRegArray(self,regIndex,npArray):
        self.__useMap()
        dtype = npArray.dtype
        if dtype == np.intc:
            self.C.getArrayInt(regIndex,ffi.cast("int *",npArray.ctypes.data))
        elif dtype == np.float:
            self.C.getArrayFloat(regIndex,ffi.cast("float *",npArray.ctypes.data))
        elif dtype == np.bool:
            self.C.getArrayBool(regIndex,ffi.cast("bool *",npArray.ctypes.data))
        else:
            raise AttributeError("Expecting int bool or float as dtype. Was %s"%dtype)
