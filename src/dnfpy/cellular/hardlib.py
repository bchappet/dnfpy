import numpy as np
from cffi import FFI

ffi = FFI()
ffi.cdef("""
    int initSimu(int width,int height,char* cellName,char* connecterName,bool wrap);
    int initSimuParam(int width,int height,char* cellName,char* connecterName,char* param,bool wrap);
    void addConnection(char *connecterName,bool wrap);
    int useMap(int idMap);

    void preCompute();
    void compute();
    void step();
    void nstep(unsigned int n);
    void synch();
    void reset();

    void initMapSeed(long int seed);

    void setMapParamInt(int index,int value);
    void setMapParamBool(int index,bool value);
    void setMapParamFloat(int index,float value);
    int getMapParamInt(int index);
    bool getMapParamBool(int index);
    float getMapParamFloat(int index);


    void setMapSubParamInt(int index,int value);
    void setMapSubParamBool(int index,bool value);
    void setMapSubParamFloat(int index,float value);
    int getMapSubParamInt(int index);
    bool getMapSubParamBool(int index);
    float getMapSubParamFloat(int index);



    void getCellAttribute(int x,int y,int index,void* value);
    void setCellAttribute(int x,int y,int index, void* value);

    void getArrayAttributeInt(int index, int* array);
    void getArrayAttributeBool(int index, bool* array);
    void getArrayAttributeFloat(int index, float* array);

    void setArrayAttributeInt(int index, int* array);
    void setArrayAttributeBool(int index, bool* array);
    void setArrayAttributeFloat(int index, float* array);


    void getArrayInt(int index,int* array);
    void setArrayInt(int index, int* array);

    void setCellInt(int x,int y,int index,int val);
    void setCellBool(int x,int y,int index,bool val);
    void setCellFloat(int x,int y,int index,float val);

    void getArraySubState(int index,int * array);
    void setArraySubState(int index,int * array);


    //to study fault tolerence of transient orpermanent single event effect
    int getTotalRegSize() ;
    void setErrorMaskFromArray(bool * bits) ;


""")



class HardLib:
    def __init__(self,sizeX,sizeY,cellType,connecterType,param=None,wrap=False):
        self.C = ffi.dlopen("libhardsimu.so")
        cellType = str.encode(cellType)
        connecterType = str.encode(connecterType)
        
        if param:
            param = str.encode(param)
            self.__idMap = self.C.initSimuParam(sizeX,sizeY,cellType,connecterType,param,wrap)
        else:
            self.__idMap = self.C.initSimu(sizeX,sizeY,cellType,connecterType,wrap)

    def addConnection(self,connecterName,wrap=False):
        self.__useMap()
        self.C.addConnection(str.encode(connecterName),wrap)

    def __useMap(self):
        self.C.useMap(self.__idMap)

    def synch(self):
        self.__useMap()
        self.C.synch();

    def preCompute(self):
        self.__useMap()
        self.C.preCompute()

    def compute(self):
        self.__useMap()
        self.C.compute()

    def step(self):
        self.__useMap()
        self.C.step();

    def nstep(self,n):
        self.__useMap()
        self.C.nstep(n);

    def reset(self):
        self.__useMap()
        self.C.reset()

    def initSeed(self,seed):
        self.__useMap()
        self.C.initMapSeed(seed)

    def getMapParam(self,idParam,dtype):
        self.__useMap()
        if dtype == int:
            return self.C.getMapParamInt(idParam)
        elif dtype == bool:
            return self.C.getMapParamBool(idParam)
        elif dtype == float:
            return self.C.getMapParamFloat(idParam)
        else:
            raise AttributeError("Expecting int bool or float as dtype. Was %s"%dtype)




    def setMapParam(self,idParam,val):
        self.__useMap()
        dtype = type(val)
        if dtype == int:
            self.C.setMapParamInt(idParam,val)
        elif dtype == bool:
            self.C.setMapParamBool(idParam,val)
        elif dtype == float:
            self.C.setMapParamFloat(idParam,val)
        elif dtype == np.float64:
            self.C.setMapParamFloat(idParam,val)
        else:
            raise AttributeError("Expecting int bool or float as dtype. %s (id: %s) was %s"%(val,idParam,dtype))

    def getMapSubParam(self,idParam,dtype):
        self.__useMap()
        if dtype == int:
            return self.C.getMapSubParamInt(idParam)
        elif dtype == bool:
            return self.C.getMapSubParamBool(idParam)
        elif dtype == float:
            return self.C.getMapSubParamFloat(idParam)
        else:
            raise AttributeError("Expecting int bool or float as dtype. Was %s"%dtype)




    def setMapSubParam(self,idParam,val):
        self.__useMap()
        dtype = type(val)
        if dtype == int:
            self.C.setMapSubParamInt(idParam,val)
        elif dtype == bool:
            self.C.setMapSubParamBool(idParam,val)
        elif dtype == float:
            self.C.setMapSubParamFloat(idParam,val)
        elif dtype == np.float64:
            self.C.setMapSubParamFloat(idParam,val)
        else:
            raise AttributeError("Expecting int bool or float as dtype. %s (id: %s) was %s"%(val,idParam,dtype))


    def getTotalRegSize(self):
        return self.C.getTotalRegSize()

    def setErrorMaskFromArray(self,npArray):
        self.C.setErrorMaskFromArray(ffi.cast("bool *",npArray.ctypes.data))



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
        elif dtype == np.float32:
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
        elif dtype == np.float32:
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
        else:
            raise AttributeError("Expecting int or bool as dtype. Was %s"%dtype)



    def getRegArray(self,regIndex,npArray):
        self.__useMap()
        dtype = npArray.dtype
        if dtype == np.intc:
            self.C.getArrayInt(regIndex,ffi.cast("int *",npArray.ctypes.data))
        else:
            raise AttributeError("Expecting intc as dtype. Was %s"%dtype)

    def setRegArray(self,regIndex,npArray):
        self.__useMap()
        dtype = npArray.dtype
        if dtype == np.intc:
            self.C.setArrayInt(regIndex,ffi.cast("int *",npArray.ctypes.data))
        else:
            raise AttributeError("Expecting intc as dtype. Was %s"%dtype)



    def getArraySubState(self,regIndex,npArrayInt):
        self.__useMap()
        self.C.getArraySubState(regIndex,ffi.cast("int *",npArrayInt.ctypes.data))

    def setArraySubState(self,regIndex,npArrayInt):
        self.__useMap()
        self.C.setArraySubState(regIndex,ffi.cast("int *",npArrayInt.ctypes.data))
