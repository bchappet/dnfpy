#ifndef SOFTSIMU_H
#define SOFTSIMU_H

#include "map2d.h"
extern "C" {
  // typedef struct module ModuleC;




/**
     * @brief initSimu init a new map and give the index of it. Should use int useMap(int idMap) before using the map.
     * @param width
     * @param height
     * @param cellName
     * @param connecterName
     * @return
     */
    int initSimu(int width,int height,char* cellName,char* connecterName);

    /**
     * @brief initSimu
     * @param width
     * @param height
     * @param cellName
     * @param connecterName
     * @param param will be given on construction of cell
     * @return
     */
    int initSimuParam(int width,int height,char* cellName,char* connecterName,char* param);


    /**
     * @brief useMap to use the specified map
     * @param idMap
     * @return
     */
    int useMap(int idMap);

    void step();
    void nstep(int n);
    void synch();
    void reset();
    void initMapSeed();


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
