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
    int initSimu(int width,int height,const char* cellName,const char* connecterName,bool wrap);

    /**
     * @brief initSimu
     * @param width
     * @param height
     * @param cellName
     * @param connecterName
     * @param param will be given on construction of cell
     * @return
     */
    int initSimuParam(int width,int height,const char* cellName,const char* connecterName,const char* param,bool wrap);
    void addConnection(char *connecterName,bool wrap);


    /**
     * @brief useMap to use the specified map
     * @param idMap
     * @return
     */
    int useMap(int idMap);

    void preCompute();
    void step();
    void nstep(unsigned int n);
    void synch();
    void reset();
    void initMapSeed(long int seed);



   // ModuleC* getCell(int x,int y);

    /**
     * @brief setMapParamInt even if stored localy parameters should be global
     * @param index
     * @param value
     * @param path
     */
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
    void getArrayBool(int index,bool * array);
    void getArrayFloat(int index,float * array);

    void setArrayInt(int index, int* array);
    void setArrayBool(int index, bool* array);
    void setArrayFloat(int index, float* array);

    void setCellInt(int x,int y,int index,int val);
    void setCellBool(int x,int y,int index,bool val);
    void setCellFloat(int x,int y,int index,float val);

    //subStates to access sub module
    void getArraySubState(int index,int * array);
    void setArraySubState(int index,int * array);

    //to study fault tolerence of transient orpermanent single event effect
    int getTotalRegSize() ;
    void setErrorMaskFromArray(bool * bits) ;

}





#endif // SOFTSIMU_H
