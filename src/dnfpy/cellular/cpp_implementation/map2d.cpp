#include "map2d.h"

#include <iostream>

Map2D::Map2D(int width,int height) : Module()
{
    this->width = width;
    this->heigth = height;

    this->cellArray = new Module**[this->heigth];
    for(int i = 0 ; i < this->heigth ; i++){
        this->cellArray[i] = new Module*[this->width];
    }
}

void Map2D::getCellAttribute(int x,int y,int index,void* value){
    return this->cellArray[y][x]->getAttribute(index,value);
}
void Map2D::setCellAttribute(int x,int y,int index,void* value){
    return this->cellArray[y][x]->setAttribute(index,value);
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




