#ifndef SOFTSIMU_H
#define SOFTSIMU_H

#include "map2d.h"
extern "C" {
  // typedef struct module ModuleC;
    extern Map2D* mapSimu;

    void initSimu(int width,int height,char* cellName,char* connecterName);

    void step();
    void nstep(int n);
    void synch();

   // ModuleC* getCell(int x,int y);

    /**
     * @brief setMapParamInt even if stored localy parameters should be global
     * @param index
     * @param value
     * @param path
     */
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

}





#endif // SOFTSIMU_H
