#ifndef SOFTSIMU_H
#define SOFTSIMU_H

#include "map2d.h"
extern "C" {
    extern Map2D* mapSimu;

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

}





#endif // SOFTSIMU_H
