#include "softsimu.h"
#include "connecter.h"
#include <iostream>


#include "cellgof.h"
#include "cellrsdnf.h"
#include "mooreconnecter.h"
#include "neumannconnecter.h"
#include "rsdnfconnecter.h"
#include "connecter.h"


void initCellArrayFromName(Map2D& map,std::string name);
void connecterFromName(Map2D& map,std::string name);

SoftSimu::SoftSimu(int width,int height,std::string cellName,std::string connecterName):
    map(width,height)
{
    initCellArrayFromName(this->map,cellName);
    connecterFromName(this->map,connecterName);
}

void SoftSimu::step(){
    this->map.compute();
    this->map.synch();
}

void SoftSimu::getArrayInt(int index,int ** array){
    this->map.getArrayState<int>(index,array);
}

void SoftSimu::getArrayBool(int index,bool** array){
    this->map.getArrayState<bool>(index,array);
}

void SoftSimu::getArrayFloat(int index,float ** array){
    this->map.getArrayState<float>(index,array);
}

void SoftSimu::setArrayInt(int index,int** array){
    return this->map.setArrayState<int>(index,array);
}

void SoftSimu::setArrayBool(int index,bool** array){
    return this->map.setArrayState<bool>(index,array);
}

void SoftSimu::setArrayFloat(int index,float** array){
    return this->map.setArrayState<float>(index,array);
}

void SoftSimu::setCellInt(int x,int y,int index,int val){
    this->map.setCellState<int>(x,y,index,val);
}

void SoftSimu::setCellBool(int x,int y,int index,bool val){
    this->map.setCellState<bool>(x,y,index,val);
}

void SoftSimu::setCellFloat(int x,int y,int index,float val){
    this->map.setCellState<float>(x,y,index,val);
}






void initCellArrayFromName(Map2D& map,std::string name){
    if(name.compare("cellgof")==0){
        map.initCellArray<CellGof>();
    }else if(name.compare("cellrsdnf")==0){
        map.initCellArray<CellRsdnf>();
    }else{
        std::cerr << "unvalid cell name " << name << std::endl;
    }
}

void connecterFromName(Map2D& map,std::string name){

    if(name.compare("mooreconnecter")==0){
        MooreConnecter c;
        map.connect(c);
    }else if(name.compare("neumannconnecter")==0){
        NeumannConnecter c;
        map.connect(c);
    }else if(name.compare("rsdnfconnecter")==0){
        RsdnfConnecter c;
        map.connect(c);
    }else{
        std::cerr << "unvalid connecter name " << name << std::endl;
    }

}
