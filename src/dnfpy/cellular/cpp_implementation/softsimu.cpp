#include "softsimu.h"
#include "connecter.h"
#include <iostream>


#include "cellgof.h"
#include "cellrsdnf.h"
#include "cellnspike.h"
#include "mooreconnecter.h"
#include "neumannconnecter.h"
#include "rsdnfconnecter.h"
#include "nspikeconnecter.h"
#include "rsdnfconnecter2layer.h"
#include "sequenceConnecter.h"
#include "connecter.h"
#include <string.h>
#include "cellbsrsdnf.h"
#include "cellsbsfast.h"
#include "cellsbsfast2.h"
#include "cellrsdnf2.h"


std::vector<Map2D*> mapSimuVec;
Map2D* mapSimu;

void initCellArrayFromName(Map2D* mapSimu,const char* name);
void initCellArrayFromNameWithParam(Map2D* map,const char* name,const char* param);
void connecterFromName(Map2D* mapSimu,const char* name,bool wrap);

int useMap(int idMap_){
    mapSimu = mapSimuVec[idMap_];
    return 0;
}

void setMapParamInt(int index,int value){
    mapSimu->setArrayParam<int>(index,value);
}

void setMapParamBool(int index,bool value){
    mapSimu->setArrayParam<bool>(index,value);
}

void setMapParamFloat(int index,float value){
    mapSimu->setArrayParam<float>(index,value);
}

int getMapParamInt(int index){
    return mapSimu->getCellParam<int>(0,0,index);
}


bool getMapParamBool(int index){
    return mapSimu->getCellParam<bool>(0,0,index);
}

float getMapParamFloat(int index){
    return mapSimu->getCellParam<float>(0,0,index);
}


void setMapSubParamInt(int index,int value){
    mapSimu->setArraySubParam<int>(index,value);
}

void setMapSubParamBool(int index,bool value){
    mapSimu->setArraySubParam<bool>(index,value);
}

void setMapSubParamFloat(int index,float value){
    mapSimu->setArraySubParam<float>(index,value);
}

int getMapSubParamInt(int index){
    return mapSimu->getCellSubParam<int>(0,0,0,index);
}


bool getMapSubParamBool(int index){
    return mapSimu->getCellSubParam<bool>(0,0,0,index);
}

float getMapSubParamFloat(int index){
    return mapSimu->getCellSubParam<float>(0,0,0,index);
}



//ModuleC* convertModuleToC(Module* mod);
int initSimu(int width,int height,const char* cellName,const char* connecterName,bool wrap)
{
    Map2D* theNewMap = new Map2D(width,height);

    initCellArrayFromName(theNewMap,cellName);

    connecterFromName(theNewMap,connecterName,wrap);
    mapSimuVec.push_back(theNewMap);
    return mapSimuVec.size()-1;
}

int initSimuParam(int width,int height,const char* cellName,const char* connecterName,const char* param,bool wrap){
    Map2D* theNewMap = new Map2D(width,height);
    initCellArrayFromNameWithParam(theNewMap,cellName,param);
    connecterFromName(theNewMap,connecterName,wrap);
    mapSimuVec.push_back(theNewMap);
    return mapSimuVec.size()-1;
}

void addConnection(char *connecterName,bool wrap){
    connecterFromName(mapSimu,connecterName,wrap);

}


void reset(){
    mapSimu->reset();
}

void synch(){
    mapSimu->synch();
}

void preCompute(){
  //  clock_t start = clock(), diff;
    mapSimu->preCompute();
   // diff = clock() - start;
  //  int msec = diff * 1000 / CLOCKS_PER_SEC;
   // printf("Precompute time taken %d seconds %d milliseconds\n", msec/1000, msec%1000);
}

void step(){
//    clock_t start = clock(), diff;
    mapSimu->compute();
    mapSimu->synch();
//    diff = clock() - start;
//    int msec = diff * 1000 / CLOCKS_PER_SEC;
//    printf("Step time taken %d seconds %d milliseconds\n", msec/1000, msec%1000);
}
void nstep(unsigned int n){
    unsigned int count;
    for(count = 0 ; count < n ; ++count){
        //for unknown reason when calling directly step, it doesnot work on python side...
        mapSimu->compute();
        mapSimu->synch();
    }
}

void initMapSeed(long int seed){
    mapSimu->initMapSeed(seed);
}


//ModuleC* getCell(int x,int y){
//    return convertModuleToC(mapSimu->getCell(x,y));
//}

//ModuleC* convertModuleToC(Module* mod){
//    //TODO
//    return new ModuleC;
//}

void getCellAttribute(int x,int y,int index,void* value){
    return mapSimu->getCellAttribute(x,y,index,value);
}

void setCellAttribute(int x,int y,int index, void* value){
    return mapSimu->setCellAttribute(x,y,index,value);
}

void getArrayAttributeInt(int index, int* array){
    return mapSimu->getArrayAttribute<int>(index,array);
}

void getArrayAttributeBool(int index, bool* array){
    return mapSimu->getArrayAttribute<bool>(index,array);
}

void getArrayAttributeFloat(int index, float* array){
    return mapSimu->getArrayAttribute<float>(index,array);
}

void setArrayAttributeInt(int index, int* array){
    return mapSimu->setArrayAttribute<int>(index,array);
}

void setArrayAttributeBool(int index, bool* array){
    return mapSimu->setArrayAttribute<bool>(index,array);
}

void setArrayAttributeFloat(int index, float* array){
    return mapSimu->setArrayAttribute<float>(index,array);
}


void getArrayInt(int index,int * array){
    mapSimu->getArrayState(index,array);
}



void setArrayInt(int index,int* array){
    return mapSimu->setArrayState(index,array);
}




void setCellInt(int x,int y,int index,int val){
    mapSimu->setCellState(x,y,index,val);
}

void setCellBool(int x,int y,int index,bool val){
    mapSimu->setCellState(x,y,index,(int)val);
}

void getArraySubState(int index,int * array){
    mapSimu->getArraySubState(index,array);
}
void setArraySubState(int index,int * array){
    mapSimu->setArraySubState(index,array);

}


int getTotalRegSize(){
 return mapSimu->getTotalRegSize();
}

void setErrorMaskFromArray(bool * bits){
    mapSimu->setErrorMaskFromArray(bits);
}


void initCellArrayFromNameWithParam(Map2D* map,const char* name,const char* param){
    if(strcmp(name,"cellbsrsdnf")==0){
        map->initCellArray<CellBsRsdnf>(param);
    }else if(strcmp(name,"cellrsdnf")==0){
        map->initCellArray<CellRsdnf>(param);
    }else{
        std::cerr << "unvalid cell name " << name << std::endl;
    }


}



void initCellArrayFromName(Map2D* map,const char* name){
    if(strcmp(name,"cellgof")==0){
        map->initCellArray<CellGof>();
    }else if(strcmp(name,"cellrsdnf")==0){
        map->initCellArray<CellRsdnf>();
    }else if(strcmp(name,"cellnspike")==0){
        map->initCellArray<CellNSpike>();
    }else if(strcmp(name,"cellbsrsdnf")==0){
        map->initCellArray<CellBsRsdnf>();
    }else if(strcmp(name,"cellsbsfast")==0){
        map->initCellArray<CellSBSFast>();
    }else if(strcmp(name,"cellsbsfast2")==0){
        map->initCellArray<CellSBSFast2>();
    }else if(strcmp(name,"cellrsdnf2")==0){
        map->initCellArray<CellRsdnf2>();
    }else{
        std::cerr << "unvalid cell name " << name << std::endl;
    }


}

void connecterFromName(Map2D* map,const char* name,bool wrap){

    if(strcmp(name,"mooreconnecter")==0){
        MooreConnecter c;
        map->connect(c,wrap);
    }else if(strcmp(name,"neumannconnecter")==0){
        NeumannConnecter c;
        map->connect(c,wrap);
    }else if(strcmp(name,"rsdnfconnecter")==0){
        RsdnfConnecter c;
        map->connect(c,wrap);
    }else if(strcmp(name,"nspikeconnecter")==0){
        NSpikeConnecter c;
        map->connect(c,wrap);
    }else if(strcmp(name,"rsdnfconnecter2layer")==0){
        RsdnfConnecter2layer c;
        map->connect(c,wrap);
    }else if(strcmp(name,"sequenceconnecter")==0){
        SequenceConnecter c;
        map->connect(c,wrap);
    }else if(strcmp(name,"sequenceconnecterShort")==0){
        SequenceConnecterShort c;
        map->connect(c,wrap);
    }else{
        std::cerr << "unvalid connecter name " << name << std::endl;
    }

}



