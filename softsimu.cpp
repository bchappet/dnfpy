#include "softsimu.h"
#include "connecter.h"
#include <iostream>


#include "cellgof.h"
#include "cellrsdnf.h"
#include "mooreconnecter.h"
#include "neumannconnecter.h"
#include "rsdnfconnecter.h"
#include "connecter.h"
#include <string.h>

Map2D* mapSimu;
void initCellArrayFromName(Map2D* mapSimu,char* name);
void connecterFromName(Map2D* mapSimu,char* name);

void initSimu(int width,int height,char* cellName,char* connecterName)
{
    mapSimu = new Map2D(width,height);
    initCellArrayFromName(mapSimu,cellName);
    connecterFromName(mapSimu,connecterName);
}

void step(){
    mapSimu->compute();
    mapSimu->synch();
}

void getArrayInt(int index,int ** array){
    mapSimu->getArrayState<int>(index,array);
}

void getArrayBool(int index,bool** array){
    mapSimu->getArrayState<bool>(index,array);
}

void getArrayFloat(int index,float ** array){
    mapSimu->getArrayState<float>(index,array);
}

void setArrayInt(int index,int** array){
    return mapSimu->setArrayState<int>(index,array);
}

void setArrayBool(int index,bool** array){
    return mapSimu->setArrayState<bool>(index,array);
}

void setArrayFloat(int index,float** array){
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
    }else{
        std::cerr << "unvalid connecter name " << name << std::endl;
    }

}
