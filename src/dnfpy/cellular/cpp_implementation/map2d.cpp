#include "map2d.h"

#include <iostream>
#include "bitstreamutils.h"
Map2D::Map2D() : Module(){
    this->params = ParamsPtr(new std::vector<void *>());
}

Map2D::~Map2D(){
}

void Map2D::initMapSeed(long int seed){
    initSeed(seed);
}


void Map2D::initMemory(int width, int height){
    this->width = width;
    this->height = height;

    this->cellArray = std::vector<std::vector<Module::ModulePtr>>(height);



    for(int i = 0 ; i < this->height ; i++){
        this->cellArray[i].resize(this->width);
    }
}

Map2D::Map2D(int width,int height) : Map2D()
{
   this->initMemory(width,height);
}

void Map2D::getCellAttribute(int x,int y,int index,void* value){
    return this->cellArray[y][x]->getAttribute(index,value);
}
void Map2D::setCellAttribute(int x,int y,int index,void* value){
    return this->cellArray[y][x]->setAttribute(index,value);
}



void Map2D::reset(){
    Module::reset();
    for(int i = 0 ; i < this->height ; i++){
        for(int j = 0 ; j < this->width ; j++){
            this->cellArray[i][j]->reset();
        }
    }
}

void Map2D::preCompute(){
//    std::cout << "precompute " << this->height  <<"x"<< this->width << std::endl;
//    std::cout << "pSpike: " <<this->getParam<float>(0) << std::endl;
//    std::cout << "sizeStream: " <<this->getParam<int>(1) << std::endl;
//    std::cout << "pExc: " <<this->getParam<float>(2) << std::endl;
//    std::cout << "precision mask: " <<this->getParam<unsigned long int>(3) << std::endl;

    Module::preCompute();
    for(int i = 0 ; i < this->height ; i++){
        for(int j = 0 ; j < this->width ; j++){
            this->cellArray[i][j]->preCompute();
        }
    }
}

void Map2D::compute(){
    Module::compute();
    for(int i = 0 ; i < this->height ; i++){
        for(int j = 0 ; j < this->width ; j++){
            this->cellArray[i][j]->compute();
        }
    }
}

void Map2D::synch(){
    Module::synch();
    for(int i = 0 ; i < this->height ; i++){
        for(int j = 0 ; j < this->width ; j++){
            this->cellArray[i][j]->synch();
        }
    }
}
   


 
