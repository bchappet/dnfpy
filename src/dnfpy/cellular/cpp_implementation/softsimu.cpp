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
#include "connecter.h"
#include <string.h>
#include "cellbsrsdnf.h"


std::vector<Map2D*> mapSimuVec;
Map2D* mapSimu;

void initCellArrayFromName(Map2D* mapSimu,char* name);
void connecterFromName(Map2D* mapSimu,char* name);

int useMap(int idMap_){
    mapSimu = mapSimuVec[idMap_];
    return 0;
}

void setMapParamInt(int index,int value,char* path){
    mapSimu->setMapParam<int>(index,value,path);
}

void setMapParamBool(int index,bool value,char* path){
    mapSimu->setMapParam<bool>(index,value,path);
}

void setMapParamFloat(int index,float value,char* path){
    mapSimu->setMapParam<float>(index,value,path);
}

int getMapParamInt(int index,char* path){
    return mapSimu->getMapParam<int>(index,path);
}


bool getMapParamBool(int index,char* path){
    return mapSimu->getMapParam<bool>(index,path);
}

float getMapParamFloat(int index,char* path){
    return mapSimu->getMapParam<float>(index,path);
}


//ModuleC* convertModuleToC(Module* mod);
int initSimu(int width,int height,char* cellName,char* connecterName)
{
    Map2D* theNewMap = new Map2D(width,height);
    initCellArrayFromName(theNewMap,cellName);
    connecterFromName(theNewMap,connecterName);
    mapSimuVec.push_back(theNewMap);
    return mapSimuVec.size()-1;
}

void reset(){
    mapSimu->reset();
}

void synch(){
    mapSimu->synch();
}

void step(){
    mapSimu->compute();
    mapSimu->synch();
}
void nstep(int n){
    for(int i = 0 ; i < n ; i++){
        step();
    }
}

void initMapSeed(){
    mapSimu->initMapSeed();
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
    mapSimu->getArrayState<int>(index,array);
}

void getArrayBool(int index,bool* array){
    mapSimu->getArrayState<bool>(index,array);
}

void getArrayFloat(int index,float* array){
    mapSimu->getArrayState<float>(index,array);
}

void setArrayInt(int index,int* array){
    return mapSimu->setArrayState<int>(index,array);
}

void setArrayBool(int index,bool* array){
    return mapSimu->setArrayState<bool>(index,array);
}

void setArrayFloat(int index,float* array){
    return mapSimu->setArrayState<float>(index,array);
}

void setCellInt(int x,int y,int index,int val){
    mapSimu->setCellState<int>(x,y,index,val);
}

void setCellBool(int x,int y,int index,bool val){
    mapSimu->setCellState<bool>(x,y,index,val);
}

void setCellFloat(int x,int y,int index,float val){
    mapSimu->setCellState<float>(x,y,index,val);
}






void initCellArrayFromName(Map2D* map,char* name){
    if(strcmp(name,"cellgof")==0){
        map->initCellArray<CellGof>();
    }else if(strcmp(name,"cellrsdnf")==0){
        map->initCellArray<CellRsdnf>();
    }else if(strcmp(name,"cellnspike")==0){
        map->initCellArray<CellNSpike>();
    }else if(strcmp(name,"cellbsrsdnf")==0){
        map->initCellArray<CellBsRsdnf>();
    }else{
        std::cerr << "unvalid cell name " << name << std::endl;
    }
}

void connecterFromName(Map2D* map,char* name){

    if(strcmp(name,"mooreconnecter")==0){
        MooreConnecter c;
        map->connect(c);
    }else if(strcmp(name,"neumannconnecter")==0){
        NeumannConnecter c;
        map->connect(c);
    }else if(strcmp(name,"rsdnfconnecter")==0){
        RsdnfConnecter c;
        map->connect(c);
    }else if(strcmp(name,"nspikeconnecter")==0){
        NSpikeConnecter c;
        map->connect(c);
    }else{
        std::cerr << "unvalid connecter name " << name << std::endl;
    }

}
