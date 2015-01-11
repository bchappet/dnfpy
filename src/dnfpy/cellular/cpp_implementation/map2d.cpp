#include "map2d.h"

#include <iostream>
#include "bitstreamutils.h"
Map2D::Map2D() : Module(){

}

void Map2D::initMapSeed(){
    initSeed();
}

void Map2D::initMemory(int width, int height){
    this->width = width;
    this->heigth = height;

    this->cellArray = new Module**[this->heigth];
    for(int i = 0 ; i < this->heigth ; i++){
        this->cellArray[i] = new Module*[this->width];
    }
}

Map2D::Map2D(int width,int height) : Module()
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
    for(int i = 0 ; i < this->heigth ; i++){
        for(int j = 0 ; j < this->width ; j++){
            this->cellArray[i][j]->reset();
        }
    }
}

void Map2D::compute(){
    Module::compute();
    for(int i = 0 ; i < this->heigth ; i++){
        for(int j = 0 ; j < this->width ; j++){
            this->cellArray[i][j]->compute();
        }
    }
}

void Map2D::synch(){
    Module::synch();
    for(int i = 0 ; i < this->heigth ; i++){
        for(int j = 0 ; j < this->width ; j++){
            this->cellArray[i][j]->synch();
        }
    }
}




